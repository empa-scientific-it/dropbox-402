
from java.io import File
from java.nio.file import Files
from java.nio.file.attribute import BasicFileAttributes
from java.text import SimpleDateFormat
from java.util import Date
import os.path as path


def format_date(date):
    """format the date to a string"""
    return SimpleDateFormat("yyyy-MM-dd HH:mm").format(date)


def is_valid(logger, file):
    """check if the file is a zip file"""

    path = file.toPath()
    fo = path.getName(path.getNameCount() -
                      1).toString().encode('ascii', 'ignore')
    return fo.endswith(".zip")


def get_name(file):
    """Get the name of the file without extension"""
    return file.toPath().getName(file.toPath().getNameCount() - 1).toString().encode('ascii', 'ignore').split(".")[0]


def get_creation_time(file):
    """Gets the creation time from the file using the Java NIO API"""
    return SimpleDateFormat("yyyymmdd").parse(get_name(file))


def process(tr):
    incoming = tr.getIncoming()
    #Get logger
    logger = tr.getLogger()
    logger.info("Incoming file: " + str(incoming.toPath()))
    logger.info("Checking if the file is valid")
    if is_valid(logger, incoming):
        # Get the creation time of the file
        data_set = tr.createNewDataSet()
        logger.info("The created dataset is:" + str(data_set.getDataSetCode()))
        # Move the file to the dataset
        # Get the search service
        search_service = tr.getSearchService()
        # List all experiments in a project
        sp_name = "SURFAC_MICHAL.GORA_AT_EMPA.CH"
        pr_name = "ESFA_EXPERIMENTS"
        experiments = search_service.getExperiment("/" + sp_name  + "/" + pr_name  + "/ESFA")
        logger.info("The experiment to upload is:" + experiments.toString())
        # Create a new sample and set its experiment
        logger.info("Creating new sample")
        smp = tr.createNewSampleWithGeneratedCode(sp_name, "EXPERIMENTAL_STEP_MILAR")
        smp.setExperiment(experiments)
        smp.setPropertyValue("START_DATE", format_date(
            get_creation_time(incoming)))
        smp.setPropertyValue("$NAME", get_name(incoming))
        # Set the dataset to the sample just created
        logger.info("Setting the dataset")
        data_set.setSample(smp)
        tr.moveFile(incoming.getAbsolutePath(), data_set)
    else:
        logger.info("The uploaded directory does not match the expected format")
