
from java.io import File
from java.nio.file import Files
from java.nio.file.attribute import BasicFileAttributes
from java.text import SimpleDateFormat
from java.util import Date

def format_date(date):
    """format the date to a string"""
    return SimpleDateFormat("yyyy-MM-dd HH:mm").format(date)

def process(tr):
    print("Started")
    data_set = tr.createNewDataSet()
    incoming = tr.getIncoming()
    print(incoming)
    #Get the creation time of the file
    creation_time = Date(Files.readAttributes(incoming.toPath(), "creationTime")['creationTime'].toMillis())
    tr.moveFile(incoming.getAbsolutePath(), data_set)
    # Get the search service
    search_service = tr.getSearchService()
 
    #List all experiments in a project
    experiments = search_service.listExperiments("/TEST/TEST")
    print(experiments[0])

    #Create a new sample and set its experiment
    smp = tr.createNewSampleWithGeneratedCode("TEST", "MEASUREMENT")
    smp.setExperiment(experiments[0])
    smp.setPropertyValue("MEASUREMENT_DATE", format_date(creation_time))
 
    # # Search for all samples with a property value determined by the file name; we don't care about the type
    # samplePropValue = incoming.getName()
    # samples = search_service.searchForSamples("ORGANISM", samplePropValue, None)
 

    data_set.setSample(smp)

 

