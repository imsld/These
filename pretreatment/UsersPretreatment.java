package org.qos.pretreatment;

import java.util.ArrayList;
import java.util.List;

import org.qos.fileHelper.CsvFileReadHelper;
import org.qos.geoLiteCity.GeoDistance;

public class UsersPretreatment {

	private List<String[]> list_user;
	private List<String[]> new_info_list_user;
	private List<String> list_rt_user;
	private List<String> new_list_user;

	private GeoDistance geoDistance;

	public UsersPretreatment() {
		System.out.println("...user préparation...");
		geoDistance = new GeoDistance();
		new_list_user = new ArrayList<String>();

		System.out.println("Récupération de la liste des users...(userlist.txt)");
		list_user = CsvFileReadHelper.getList(_Pretreatment.USER_FILE_PATH, true);
		System.out.println("Récupération de la liste des users...(rtdata.txt)");
		list_rt_user = CsvFileReadHelper.get_rt_UserList(_Pretreatment.RTDATA_FILE);
		System.out.println("Vérification des users");
		check_Users();
		newUserListFile();
	}

	private void newUserListFile() {

		new_info_list_user = new ArrayList<String[]>();
		list_user.stream().forEach(item -> {
			if (item[0].compareTo("-1") != 0) {
				new_info_list_user.add(item);
				new_list_user.add(item[0]);
			}
		});
	}

	private void check_Users() {
		for (String[] strings : list_user) {
			String user = strings[0];
			String ip = strings[1];
			if (geoDistance.getLocation(ip) == null) {
				strings[0] = "-1";
				continue;
			}
			if (!list_rt_user.contains(user)) {
				strings[0] = "-1";
				continue;
			}
			strings[5] = String.valueOf(geoDistance.getLatitude());
			strings[6] = String.valueOf(geoDistance.getLongitude());
		}
	}

	public List<String[]> getNew_info_list_user() {
		return new_info_list_user;
	}

	public List<String> getNew_list_user() {
		return new_list_user;
	}
	
	public int getTotalOldUsers(){
		return list_user.size();
	}
	
	public int getTotalNewUsers(){
		return new_list_user.size();
	}
}
