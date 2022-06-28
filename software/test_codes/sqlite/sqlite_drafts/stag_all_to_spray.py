import software.test_codes.sqlite.sqlite_drafts.lib_pcf_ver4 as pcf

pcf.logging.basicConfig(filename = 'staging_log_%s.log'%str(pcf.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")), level = pcf.logging.DEBUG, format='[%(filename)s:%(lineno)s - %(funcName)20s() ] %(asctime)s %(message)s')


try:
    pcf.print_log("Start Staging all cows from zero table to spray table")
    pcf.Staging_Into_Spray_Table()
except Exception as e:
    pcf.print_log("Error in staging function", e)
else:
    pcf.print_log("Success: Main functrion of staging worked well")