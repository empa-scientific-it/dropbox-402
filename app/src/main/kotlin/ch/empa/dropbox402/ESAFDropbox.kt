package ch.empa.dropbox402

import ch.systemsx.cisd.etlserver.registrator.api.v2.AbstractJavaDataSetRegistrationDropboxV2
import ch.systemsx.cisd.etlserver.registrator.api.v2.IDataSetRegistrationTransactionV2
import org.apache.poi.xwpf.usermodel.XWPFDocument
import java.io.File
import java.io.FileInputStream
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

import ch.systemsx.cisd.openbis.dss.generic.shared.IEncapsulatedOpenBISService;



fun isValid(f: File): Boolean {
    return f.nameWithoutExtension.matches(Regex("\\d{8}")) && f.isDirectory
}

fun findInfo(f: File): File? {
    return f.listFiles { it -> it.name == "${f.name}.doc" }.getOrNull(0)
}

fun getDateFromName(s: String): LocalDate {
    val fmt = DateTimeFormatter.ofPattern("yyyymmdd")
    return LocalDateTime.parse(s, fmt).toLocalDate()
}

fun formatDate(d: LocalDate): String {
    val fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")
    return fmt.format(d)
}

fun getFileContent(f: File): String{
    val fis = FileInputStream(f)
    val document = XWPFDocument(fis)
    return document.paragraphs.map {  it.text }.reduce{ ac, cur -> ac + cur}
}

class ESAFDropbox : AbstractJavaDataSetRegistrationDropboxV2() {
    override fun process(transaction: IDataSetRegistrationTransactionV2?) {
        //Get logger
        val logger = transaction?.logger
        logger?.info("Started dropbox script")
        val incoming = transaction?.incoming

        logger?.info("Incoming file: ${incoming?.toPath()}")
        logger?.info("Checking if the file is valid")
        if (incoming != null && isValid(incoming)) {
            val infoFile = findInfo(incoming)
            val searchService = transaction.searchService
            //Find the experiment with the needed name
            val spName = "SURFAC_MICHAL.GORA_AT_EMPA.CH"
            val prName = "ESFA_EXPERIMENTS"
            val experiments = searchService.getExperiment("/${spName}/${prName}/ESFA")
            logger?.info("The experiment to upload is:$experiments")
            //Create a new sample and set its experiment
            logger?.info("Creating new sample")
            val smp = transaction.createNewSampleWithGeneratedCode(spName, "EXPERIMENTAL_STEP_MILAR")
            smp.experiment = experiments
            //Set the start date property
            smp.setPropertyValue(
                "START_DATE", formatDate(
                    getDateFromName(incoming.nameWithoutExtension)
                )
            )
            smp.setPropertyValue("\$NAME", incoming.nameWithoutExtension)
            //If a doc file is attached, write the contents
            if(infoFile != null){
                smp.setPropertyValue("EXP_DESCRIPTION", getFileContent(infoFile))
            }
            //Set the dataset to the sample just created
            val dataset = transaction.createNewDataSet()
            logger?.info("Setting the dataset")
            dataset.sample = smp
            transaction.moveFile(incoming.absolutePath, dataset)
        }
    }
}