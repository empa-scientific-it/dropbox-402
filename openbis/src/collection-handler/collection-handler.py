
from java.io import File
from java.nio.file import Files
from java.nio.file.attribute import BasicFileAttributes
from java.text import SimpleDateFormat
from java.util import Date
import zipfile


def format_date(date):
    """format the date to a string"""
    return SimpleDateFormat("yyyy-MM-dd HH:mm").format(date)

def is_zip(file):
    """check if the file is a zip file"""
    return file.getName().endswith(".zip")

def get_creation_time(file):
    """Gets the creation time from the file using the Java NIO API"""
    return  Date(Files.readAttributes(file.toPath(), "creationTime")['creationTime'].toMillis())


def process(tr):
    print("Started")
    data_set = tr.createNewDataSet()
    incoming = tr.getIncoming()
    if is_zip(incoming):
    #Get the creation time of the file
        tr.moveFile(incoming.getAbsolutePath(), data_set)
        # Get the search service
        search_service = tr.getSearchService()
    
        #List all experiments in a project
        experiments = search_service.listExperiments("/TEST/TEST")
        print(experiments[0])

        #Create a new sample and set its experiment
        smp = tr.createNewSampleWithGeneratedCode("TEST", "MEASUREMENT")
        smp.setExperiment(experiments[0])
        smp.setPropertyValue("MEASUREMENT_DATE", format_date(get_creation_time(incoming)))
        #Set the dataset to the sample just created
        data_set.setSample(smp)

 

