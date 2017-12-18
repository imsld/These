package org.qos.pretreatment;

import java.util.List;

import org.qos.fileHelper.CsvFileReadHelper;
import org.qos.fileHelper.CsvFileWriteHelper;
import org.qos.model.User;
import org.qos.prediction.initUsers;

public class RtDataPretreatment {

	public RtDataPretreatment(List<String> user, List<String> service) {
		System.out.println("...rtdata préparation...");
		System.out.println("Création du nouveau rtdata.txt...");
		CsvFileReadHelper.create_newRTData(_Pretreatment.RTDATA_FILE, user, service);
	}

	public void createUserRtDataFile(List<String> new_list_user) {
		System.out.println("Création des fichiers contenant la liste des rtData pour chaque user");
		for (String user : new_list_user) {
			StringBuilder result = CsvFileReadHelper.getUserAllRtData(user);
			System.out.println("Création des rtData du user : " + user);
			CsvFileWriteHelper.saveUserNewFiles(Integer.parseInt(user), result, _Pretreatment.USER_RTDATA_PATH);
		}
	}

	public void createUserServicesFile(List<String> new_list_user, List<String> new_list_service) {
		System.out.println("Création des fichiers contenant la liste des services pour chaque user");
		for (String user : new_list_user) {
			StringBuilder result = CsvFileReadHelper.getUserAllServices(user, new_list_service);
			System.out.println("Création des services du user : " + user);
			CsvFileWriteHelper.saveUserNewFiles(Integer.parseInt(user), result, _Pretreatment.USER_SERVICES_PATH);
		}

	}

	public void createUserServiceCompleteSlotFiles() {
		System.out.println(
				"Création des fichiers contenant la liste des services avec 64 slots valides pour chaque user");
		initUsers users = new initUsers();
		List<User> list_user = users.getList_user();

		int total_slot = 0;
		int total_count = 0;

		for (User user : list_user) {
			int count = 0;
			StringBuilder list_complete_slot = new StringBuilder();
			for (String service_id : user.getServicesList()) {
				if (user.getServicesList().contains(service_id)) {
					List<Double> list = user.getServiceRtDataList(Integer.parseInt(service_id));
					boolean trouve = false;
					for (Double float1 : list) {
						if (float1 == -1) {
							trouve = true;
							break;
						}
					}
					if (!trouve) {
						list_complete_slot.append(service_id);
						list_complete_slot.append('\n');
						count++;
					}
				}
			}
			total_slot += user.getServicesList().size();
			total_count += count;
			int slot = user.getServicesList().size();
			String str = count + "/" + slot;
			System.out.println("Création des services du user : " + user.getUser_ID() + " " + str + " -"
					+ (slot - count) + " (" + (count * 100 / slot) + ")");
			CsvFileWriteHelper.saveUserNewFiles(user.getUser_ID(), list_complete_slot,
					_Pretreatment.USER_SERVICE_COMPLETE_SLOT_PATH);
		}
		System.out.println("Total: " + total_count + "/" + total_slot + " (" + (total_count * 100 / total_slot) + ")");
	}

}
