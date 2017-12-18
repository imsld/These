package org.qos.pretreatment;


import org.qos.fileHelper.CsvFileWriteHelper;

public class _Pretreatment {
	public static int TOTAL_SERVICE = 4500;
	public static final String USER_FILE_PATH = "Dataset/dataset1/userlist.txt";
	public static final String NEW_USER_FILE_PATH = "Dataset/dataset1/_new_userlist.txt";
	public static final String USER_SERVICES_PATH = "Dataset/dataset1/_userServices/";
	public static final String USER_SERVICE_COMPLETE_SLOT_PATH = "Dataset/dataset1/_userServicesCompeteSlot/";

	public static final String SERVICE_FILE_PATH = "Dataset/dataset1/wslist.txt";
	public static final String NEW_SERVICE_FILE_PATH = "Dataset/dataset1/_new_wslist.txt";

	public static final String RTDATA_FILE = "Dataset/dataset2/rtdata.txt";
	public static final String NEW_RTDATA_FILE = "Dataset/dataset2/_new_rtdata.txt";
	public static final String USER_RTDATA_PATH = "Dataset/dataset2/_userRtData/";
	
	
	public static final String RESULT_0_500_FILE = "Dataset/result/1_0_500.txt";
	public static final String RESULT_500_1000_FILE = "Dataset/result/2_500_1000.txt";
	public static final String RESULT_1000_1500_FILE = "Dataset/result/3_1000_1500.txt";
	public static final String RESULT_1500_2000_FILE = "Dataset/result/4_1500_2000.txt";
	public static final String RESULT_2000_2500_FILE = "Dataset/result/5_2000_2500.txt";
	

	public static void main(String[] args) {
		long time = System.currentTimeMillis();

		UsersPretreatment user = new UsersPretreatment();
		CsvFileWriteHelper.saveList(user.getNew_info_list_user(), NEW_USER_FILE_PATH);

		ServicesPretreatment service = new ServicesPretreatment();
		CsvFileWriteHelper.saveList(service.getNew_info_list_service(), NEW_SERVICE_FILE_PATH);

		RtDataPretreatment rtData = new RtDataPretreatment(user.getNew_list_user(), service.getNew_list_service());
		rtData.createUserServicesFile(user.getNew_list_user(), service.getNew_list_service());
		rtData.createUserRtDataFile(user.getNew_list_user());
		
		rtData.createUserServiceCompleteSlotFiles();

		System.out.println("***************** Statistiques ******************");
		System.out.println("Nbr. user initial/Final : " + user.getTotalOldUsers() + " / " + user.getTotalNewUsers());
		System.out.println("Nbr. service initial/Final : " + service.getTotalOldServices() + " / "
				+ service.getTotalNewServices());

		System.out.println("temps total : " + (System.currentTimeMillis() - time));
	}
}
