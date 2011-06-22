#Name: General Tools:PDB Electron Density Maps... 
#Command: pythonrun pdb_density_map.show_panel 
__doc__ == """
A script to generate the required files to view a pdb structure with
electron density maps.

2Fo-Fc and Fo-Fc maps are calculated.  Maestro cmd and smap files are
produced to simplify importing the information into a Maestro session.

"""


################################################################################
# Packages 
################################################################################
import schrodinger.structure as structure
import schrodinger.structutils.analyze as analyze
import schrodinger.structutils.transform as transform
import schrodinger.job.jobcontrol as jobcontrol
import schrodinger.job.launcher as launcher
import schrodinger.utils.cmdline as cmdline
import schrodinger.utils.fileutils as fileutils
import schrodinger.utils.log as log
import random
import urllib2
import sys
import os
import re
import schrodinger.ui.qt.appframework as appframework
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
try:
    import schrodinger.maestro.maestro as maestro
    in_maestro = True
except ImportError:
    in_maestro = False 


################################################################################
# Globals 
################################################################################
_version = "$Revision: 1.2 $"
MAP_COEFFS = ['both', 'FoFc', '2FoFc']
OMIT_LIG_ADJUST = ['none', 'jiggle'] # TODO: Add coord+bfact space*.'refine'
pdb_density_map_app = None 
URL_PATTERN = "http://www.rcsb.org/pdb/files/%s"
CELL_A_PROP = 'r_pdb_PDB_CRYST1_a'  
CELL_B_PROP = 'r_pdb_PDB_CRYST1_b'  
CELL_C_PROP = 'r_pdb_PDB_CRYST1_c'  
CELL_ALPHA_PROP = 'r_pdb_PDB_CRYST1_alpha'
CELL_BETA_PROP = 'r_pdb_PDB_CRYST1_beta'  
CELL_GAMMA_PROP = 'r_pdb_PDB_CRYST1_gamma'
SPG_PROP = 's_pdb_PDB_CRYST1_Space_Group'


################################################################################
# Logging 
################################################################################
logger = log.get_output_logger('pdb_density_maps')
logger.setLevel(log.INFO)


################################################################################
# Functions
################################################################################

def show_panel():
    """
    Displays a simple GUI for this task.

    """

    global pdb_density_map_app
    if pdb_density_map_app:
        pdb_density_map_app.show()
        pdb_density_map_app.raise_()
    else:
        pdb_density_map_app = PdbEdensityMapApp()
        pdb_density_map_app.show()

    # Start event loop if we this is a stand-alone invocation.
    if not in_maestro:
        pdb_density_map_app.exec_()

    return


################################################################################
#  Functions
################################################################################
def get_parser():
    """
    @return:
        a SingleDashOptionParser configured for this application.
    @rtype:
        cmdline.SingleDashOptionParser

    """

    script_usage = "%prog <pdb_code> [<options>]"
    script_desc = "Prepares electron density maps after downloading required files."

    parser = cmdline.SingleDashOptionParser(
        usage=script_usage,
        description=script_desc,
        version_source=_version
    )
    parser.add_option(
        '-jobname',
        dest='jobname',
        default="pdb_density_map_job",
        help="Optional jobname for intermediate IO."
    )
    parser.add_option(
        '-omit_ligands',
        action='store_true',
        dest='omit_ligands',
        help="Optionally auto-detect putative ligands, remove them from the model, then calculate maps."
    )
    parser.add_option(
        '-omit_ligands_adjust',
        choices=OMIT_LIG_ADJUST,
        default="none",
        dest='omit_ligands_adjust',
        help="Optionally adjust the remaining atom coordinates to remove bias/memory of the omitted ligand(s).  Default is 'none'.  Must be one of %s.  'none' does not make any changes, 'jiggle' adds a small amount of random scatter to the remaining coordinates." % "|".join(OMIT_LIG_ADJUST)
# TODO:  add coord+bfact refinement.
#        help="Optionally adjust the remaining atom coordinates to remove bias/memory of the omitted ligand(s).  Must be one of %s.  'none' does not make any changes, 'jiggle' adds a small amount of random scatter to the remaining coordinates, 'refine' performs a reciprocal space refinement on the remaining atoms." % "|".join(OMIT_LIG_ADJUST)
    )
    parser.add_option(
        '-composite_omit',
        type=float,
        default=0.0,
        dest='composite_omit',
        help="Calculate a composite omit map by iteratively removing <composite_omit> percentage chunks of the model and assembling the mosaic of maps.  This is slower but can be less sensitive to model bias." 
    )
    parser.add_option(
        '-mapcoeff',
        dest='mapcoeff',
        choices=MAP_COEFFS,
        help="Map coefficients.  Must be one of %s" % "|".join(MAP_COEFFS)
    )
    cmdline.add_jobcontrol_options(parser)
    return parser


################################################################################
# Classes 
################################################################################
class PdbEdensityMapApp(appframework.AppFramework):
    """
    Appframework-based panel for simple electron density map calculations.

    
    """

    def __init__(self):
        import pdb_density_map_dir.pdb_density_map_ui as pdb_density_map_ui
        appframework.AppFramework.__init__(
            self,
            title="PDB Electron Density Map",
            ui=pdb_density_map_ui.Ui_Form(),
            buttons = {
                'start': {
                    'command' : self.start,
                    'precommand':self.checkValues,
                    'dialog' : 1,
                },
                'close' : {
                    'command' : self.closePanel 
                },
            },
            dialogs = {
                'start': {
                    'jobname' : 'pdb_density_map',
                    'default_disp': appframework.DISP_APPEND,
                    'incorporation':True, 
                    'default_disp': appframework.DISP_APPEND,
                    'host':True, 
                },
            }
        )
        self.ui.pdb_lineedit.setMaxLength(4)
        self.ui.regular_radiobutton.toggle()
        self.ui.two_fo_minus_fc_checkbox.setChecked(True)
        self.ui.fo_minus_fc_checkbox.setChecked(True)
        return


    def start(self):                
        """
        Runs the enrichment calculation job and populates the text area
        with the results.

        """

        pdb_code = str(self.ui.pdb_lineedit.text())
        if not pdb_code.strip():
            self.info("Please enter a four character pdb code.")
            return

        script_args = ['run', __file__, pdb_code]
        fo_fc = self.ui.fo_minus_fc_checkbox.isChecked()
        two_fo_fc = self.ui.two_fo_minus_fc_checkbox.isChecked() 
        if fo_fc and two_fo_fc:
            script_args.extend(['-mapcoeff', 'both'])
        elif two_fo_fc and not fo_fc:
            script_args.extend(['-mapcoeff', '2FoFc'])
        elif fo_fc and not two_fo_fc:
            script_args.extend(['-mapcoeff', 'FoFc'])
        else:
            self.info("At least one map coeffient type must be checked.")
            return

        if self.ui.omit_ligands_checkbox.isChecked():
            script_args.append('-omit_ligands')

        if self.ui.composite_radiobutton.isChecked():
            script_args.extend(['-composite_omit', '5.0'])

        # Add -HOST, -DISP, -PROJ 
        script_args.extend(self.jobparam.commandLineArgs()) 
        job = jobcontrol.launch_job(script_args)
        self.monitorJob(job.job_id)
        return


    def checkValues(self):
        """ 
        @return:
            0 if GUI fields have good values. 1 if fields are no suitable.
        @rtype:
            boolean

        """
        
        fo_fc = self.ui.fo_minus_fc_checkbox.isChecked()
        two_fo_fc = self.ui.two_fo_minus_fc_checkbox.isChecked() 
        if not (fo_fc or two_fo_fc):
            self.info("At least one map coeffient type must be checked.")
            return 1

        return 0


class PdbEdensityMapDriver:
    """
    A class to drive PrimeX electron density map generation including
    the downloading of input files and running the calculations.

    API example::
        # It is not a sucker, it's a blow-pop.
        pdbedenmap = PdbEdensityMapDriver('1ete', 'regular_map_job')
        pdbedenmap.run()

    @ivar composite_omit:
        Percentage of the model to remove each iteration of the composite
        omit map generation.  By default the percentage is 0.0 and a
        regular map is generated.
    @type composite_omit:
        float

    @ivar omit_ligands:
        If True then remove putative ligands from the model, jiggle
        slightly to remove bias (McRee), and calculate the omit maps.
        Default is False.
    @type omit_ligands:
        boolean

    @ivar pdb_file_name:
        Name of the downloaded structure file.
    @type pdb_file_name:
        string

    @ivar sf_file_name:
        Name of the downloaded structure factor (reflection) file.
    @type sf_file_name:
        string

    """

    def __init__(self, pdb_code, jobname='pdb_density_map_job'):
        """
        @param pdb_code:
            Four character PDB code.
        @type pdb_code:
            string
            
        @param jobname:
            Base name for intermediate IO.
        @type jobname:
            string

        """

        self.pdb_code = pdb_code
        self.jobname = jobname
        self.composite_omit = 0.0
        self.mapcoeff = 'both'
        self.omit_ligands = False
        return


    def downloadSFFile(self):
        """
        @return:
            Name of CNS format reflection file associated with pdb_code.
            If file conversion is not successful it returns None.
        @rtype:
            string

        Makes a cwd copy of the Structure Factor file for the passed
        pdb_code.  Uses refconvert to convert mmCIF to CNS.  Not every
        pdb has structure factor files deposited, and not every structure
        factor file will convert perfectly.

        """

        # Create a file name for the output.
        self.sf_file_name = "r%ssf.ent" % self.pdb_code.lower()
        download_success = None 
        logger.info(
            "Downloading structure factor file %s..." % self.sf_file_name
        )

        # Sanity check the http code from the returned html.
        http_404_re = re.compile(r'HTTP Status 404')

        # Get the raw file from RCSB http server.
        url = URL_PATTERN %  self.sf_file_name 
        try:
            url_fh = urllib2.urlopen(url)
            url_string = "".join(url_fh)
        except urllib2.HTTPError: 
            logger.warn(
                "Failed to download structure factors for %s" % self.pdb_code
            )
            return download_success 
        # Print to file.
        sf_fh = open(self.sf_file_name, mode='w')
        sf_fh.write(url_string)
        sf_fh.flush()
        sf_fh.close()
        basename = os.path.splitext(self.sf_file_name)[0]
        refconvert_exe = os.path.join(
            os.environ.get('SCHRODINGER'),
            'utilities',
            'refconvert'
        )
        cmd_args = [
            refconvert_exe, 
            '-icif',
            "%s.ent" % basename,
            '-ocns',
            "%s.cv" % basename,
        ]
        os.system(" ".join(cmd_args))
        if os.path.isfile(self.sf_file_name):
            download_success = self.sf_file_name
        return download_success 


    def downloadPDBFile(self, biological_unit=False):
        """
        @return:
            True if a download the pdb record from NIH into the cwd succeeds.
        @rtype:  boolean

        @param biological_unit:
            If True, and the file needs to be downloaded, then download
            the file at the biological unit URL, otherwise use the typical
            record URL.  Default is False, get the standard record.
        @type biological_unit:
            boolean

        """

        download_success = None
        self.pdb_file_name = "%s.pdb"% self.pdb_code
        if biological_unit:
            # The native file name is 'xxxx.pdb1.gz'.
            self.pdb_file_name = "%s.pdb1.gz" % self.pdb_code
        logger.info("Downloading %s.pdb..." % self.pdb_code)

        url = URL_PATTERN %  self.pdb_file_name
        pdb_fh = open(self.pdb_file_name,'w')
        req=urllib2.Request(url)
        try:
            fd=urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            msg = "Failed to download PDB\n" + e.__str__()
            logger.warning(msg)
            return download_success 
        except urllib2.URLError, e:
            msg = "Failed to download PDB\n" + e.__str__()
            logger.warning(msg)
            return download_success 

        a = 1
        while 1:
            data = fd.read(8092)
            # check only in first block for 'Error:'
            if a == 1:
                pos = data.find("Error:")
                if (pos >= 0) :
                    logger.info(
                        "Unable to locate an entry for PDB structure: '%s'" % (
                            self.pdb_code
                        )
                    )
                    return download_success 
                a+=1
            if not len(data):
                break
            pdb_fh.write(data)
        pdb_fh.close()

        if biological_unit:
            fd = gzip.open(self.pdb_file_name, 'rb')
            bio_pdb_file_name = os.path.splitext(self.pdb_file_name)[0]
            bio_pdb_fh = open(bio_pdb_file_name,'w')
            for line in fd:
                bio_pdb_fh.write(line)
            bio_pdb_fh.close()
            os.remove(self.pdb_file_name)
            self.pdb_file_name = bio_pdb_file_name

        download_success = os.path.isfile(self.pdb_file_name)
        return download_success


    def jiggleStructure(self, st, x_range=0.2, y_range=0.2, z_range=0.2):
        """
        Adjusts each atom position by a small, non-zero, random amount
        along +/-x,  +/-y, +/-z.

        @param st:
            The structure to manipulate.
        @type st:
            structure.Structure

        @param x_range:
            The maximum amplitude of a change, in units of angstrom.
            Each coordinate change will be within -x_range and +x_range.
        @type x_range:
            float

        @param y_range:
            The maximum amplitude of a change, in units of angstrom.
            Each coordinate change will be within -y_range and +y_range.
        @type y_range:
            float

        @param z_range:
            The maximum amplitude of a change, in units of angstrom.
            Each coordinate change will be within -z_range and +z_range.
        @type z_range:
            float

        McRee suggests a value near 0.25 angstroms for removing model
        bias from omit difference maps.

        """

        for atom in st.atom:
            x_sign = 1
            if random.random() < 0.5:
                x_sign = -1
            y_sign = 1
            if random.random() < 0.5:
                y_sign = -1
            z_sign = 1
            if random.random() < 0.5:
                z_sign = -1
            x_rand = x_range * random.random() * x_sign
            y_rand = y_range * random.random() * y_sign
            z_rand = z_range * random.random() * z_sign
            transform.translate_structure(
                st,
                x_rand,
                y_rand,
                z_rand,
                [atom.index]
            )
        return


    def writePrimeXCreateMapInputFile(self):
        """
        @return:
            The name of PrimeX map generation input file.
        @rtype:
            string

        """

        input_pdb_file = "%s.pdb" % self.pdb_code
        input_file = "primex_%s.inp" % self.jobname
        input_struct_file = "%s.mae" % self.jobname
        input_hkl_file = "r%ssf.cv" % self.pdb_code
        st = structure.StructureReader(input_pdb_file).next()
        if self.omit_ligands:
            self._removeLigands(st)
        st.write(input_struct_file)
        spg = st.property.get(SPG_PROP)
        cell_a = st.property.get(CELL_A_PROP)
        cell_b = st.property.get(CELL_B_PROP)
        cell_c = st.property.get(CELL_C_PROP)
        cell_alpha = st.property.get(CELL_ALPHA_PROP)
        cell_beta = st.property.get(CELL_BETA_PROP)
        cell_gamma = st.property.get(CELL_GAMMA_PROP)
        kwargs = """
PRIMEX_TYPE	MAP_GEN
STRUCT_FILE %s	
USE_SGB		no
MAX_FFT_MEM	400.00
PLANARITY_RESTRAINT	normal
XRES_LOW	50.00
XRES_HIGH	0.10
SOLV_MOD	mask
VDW_RAD		1.40
ION_RAD		0.80
SHR_FACT	1.40
BFAC_SCALE	aniso
MAP_WEIGHT	sigma
MAP_EXTENT	mol
GRID_SPACE	0.33
MAP_BUFFER	4.00
SCALE_MAP	yes
SPACE_GRP   %s	
CELL_A	    %.f	
CELL_B	    %.f  	
CELL_C	    %.f	
CELL_ALPHA  %.f	
CELL_BETA   %.f	
CELL_GAMMA  %.f	
REFLECT_FILE    %s	
REFLECT_FORM	cns
        """ % (
            input_struct_file,
            spg,
            cell_a,
            cell_b,
            cell_c,
            cell_alpha,
            cell_beta,
            cell_gamma,
            input_hkl_file
        )
        if self.composite_omit == 0.0:
            kwargs = kwargs + "\nMAP_TYPE	reg"
        else:
            kwargs = kwargs + "\nMAP_TYPE	comp"
            kwargs = kwargs + "\nOMIT_DATA  %.2f" % self.composite_omit
            kwargs = kwargs + "\nOMIT_TYPE  bhat-cohen"
            
        if self.mapcoeff == 'FoFc':
            kwargs = kwargs + """\nMAP_COEFF_0	1_1"""
        elif self.mapcoeff == '2FoFc':
            kwargs = kwargs + """\nMAP_COEFF_0	2_1"""
        else:
            kwargs = kwargs + """\nMAP_COEFF_0	1_1"""
            kwargs = kwargs + """\nMAP_COEFF_1	2_1"""

        inp_fh= open(input_file, 'w')
        inp_fh.write(kwargs)
        inp_fh.close()
        return input_file


    def _removeLigands(self, st):
        logger.info("Removing ligands...") 
        als = analyze.AslLigandSearcher()
        index_prop = 'i_user_secret_squirrel_index'
        for index, atom in enumerate(st.atom, start=1):
            atom.property[index_prop] = index
        ligs = als.search(st)
        ligand_atom_indexes = []
        for ligand in als.search(st):
            logger.info("Removing ligand: %s" % ligand.unique_smiles)
            lig_st = ligand.st
            for atom in lig_st.atom:
                ligand_atom_indexes.append(atom.property[index_prop])
        st.deleteAtoms(ligand_atom_indexes)
        if self.omit_ligands_adjust == 'none':
            logger.info("No change to remaining atom coordinates.")
        else:
            logger.info("Adding tiny amount of random scatter to coordinates.")
            logger.info("This reduces residual model bias from missing atoms.")
            self.jiggleStructure(st)
# TODO:  add coord+bfact refinement.
#        else:
#            logger.info("Refining coordinates and bfactors.")
#            self.refineStructure(st)
        logger.info("Done removing ligands...") 
        return


    def run(self):
        """
        Downloads, calculates, and prepares the pdb, cif, cns, smap,
        and cmd files to view a pdb structure and electron density maps.

        """

        cmd_file_name = "%s.cmd" % self.jobname
        if not (self.downloadPDBFile() and self.downloadSFFile()):
            logger.info("Failed to download the required files.")
            return

        inp_file = self.writePrimeXCreateMapInputFile()
        logger.info("Running PrimeX map generation job...")
        px_job = jobcontrol.launch_job(["primex", inp_file])
        px_job.wait()
        if not px_job.succeeded():
            logger.info("PrimeX map generation failed.")
            return
        this_jobbe = jobcontrol.get_backend()
        launch_dir = os.getcwd()
        if this_jobbe:
            # SMAP needs a path for the files, which will the launch
            # dir when jobcontrol has copied them back.
            launch_dir = this_jobbe.getJob().Dir 
            # This job only outputs maps.
            for map_file in px_job.OutputFiles:
                this_jobbe.addOutputFile(map_file)

        mae_file_name = "%s.mae" % self.jobname
        mae_file_path = os.path.join(launch_dir, mae_file_name)
        smap_file_name = "%s.smap" % self.jobname
        smap_fh = open(smap_file_name, 'w')
        smap = """# smap version 1.0
%s
primex_%s-out-1.cns:1
primex_%s-out-0.cns:1
#end
    """ % (mae_file_name, self.jobname, self.jobname) 
        smap_fh.write(smap)
        smap_fh.close()

        cmd_fh = open(cmd_file_name, 'w')
        # smap mechanism seem to need abs paths to trigger extradata.
        cmd_fh.write('entryimport extradata=true "%s"\n' % mae_file_path)
        cmd_fh.write('showpanel managesurfaces\n')
        cmd_fh.write('fit\n')
        cmd_fh.close()
        if this_jobbe:
            this_jobbe.setStructureOutputFile(mae_file_name)
            this_jobbe.addOutputFile(mae_file_name)
            this_jobbe.addOutputFile(cmd_file_name)
            this_jobbe.addOutputFile(smap_file_name)
        logger.info("Run this command file within Maestro: %s" % cmd_file_name)
        return


################################################################################
# Main
################################################################################
if __name__ == '__main__':

    parser = get_parser()
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error("Exactly one PDB code argument is required")
    if opts.nojobid:
        pemd = PdbEdensityMapDriver(args[0], opts.jobname)
        pemd.omit_ligands = opts.omit_ligands
        pemd.composite_omit = opts.composite_omit
        pemd.mapcoeff = opts.mapcoeff
        pemd.omit_ligands_adjust = opts.omit_ligands_adjust
        pemd.run()
    else:
        script_args = sys.argv[1:]
        script_args.append('-NOJOBID') # Make sure we run in 'driver' mode.
        launcher.launch(
            script=__file__,
            jobname=opts.jobname,
            args=script_args,
            wait=opts.wait,
            local=opts.local,
        )
# EOF
