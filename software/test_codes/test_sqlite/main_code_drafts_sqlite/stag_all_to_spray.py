import lib_pcf_ver45 as pcf

pcf.logging.basicConfig(filename = 'staging_log_%s.log'%str(datetime.now().strftime("%Y-%m-%d_%H_%M_%S")), level = logging.DEBUG, format='[%(filename)s:%(lineno)s - %(funcName)20s() ] %(asctime)s %(message)s')


try:
    pcf.print_log("Start Staging all cows from zero table to spray table")
    pcf.Staging_Into_Spray_Table()
except Exception as e:
    pcf.print_log("Error in staging function", e)
else:
    pcf.print_log("Success: Main functrion of staging worked well")
    return 0