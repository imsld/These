package org.qos.pretreatment;

import java.util.ArrayList;
import java.util.List;

import org.qos.fileHelper.CsvFileReadHelper;
import org.qos.geoLiteCity.GeoDistance;

public class ServicesPretreatment {

	private List<String[]> list_service;
	private List<String[]> new_info_list_service;
	private List<String> list_rt_service;
	private List<String> new_list_service;

	private GeoDistance geoDistance;

	public ServicesPretreatment() {
		System.out.println("...service préparation...");
		geoDistance = new GeoDistance();
		new_list_service = new ArrayList<String>();

		System.out.println("Récupération de la liste des services...(wslist.txt)");
		list_service = CsvFileReadHelper.getList(_Pretreatment.SERVICE_FILE_PATH, true);
		System.out.println("Récupération de la liste des services...(rtdata.txt)");
		list_rt_service = CsvFileReadHelper.get_rt_ServiceList(_Pretreatment.RTDATA_FILE);
		System.out.println("Vérification des services");
		check_Services();
		newServiceListFile();

	}

	private void newServiceListFile() {
		new_info_list_service = new ArrayList<String[]>();
		list_service.stream().forEach(item -> {
			if (item[0].compareTo("-1") != 0) {
				new_info_list_service.add(item);
				new_list_service.add(item[0]);
			}
		});
	}

	private void check_Services() {
		for (String[] strings : list_service) {
			String service = strings[0];
			String ip = strings[3];
			if (!list_rt_service.contains(service)) {
				strings[0] = "-1";
				continue;
			}
			if (geoDistance.getLocation(ip) == null) {
				strings[0] = "-1";
				continue;
			}

			strings[7] = String.valueOf(geoDistance.getLatitude());
			strings[8] = String.valueOf(geoDistance.getLongitude());
		}
	}

	public List<String[]> getNew_info_list_service() {
		return new_info_list_service;
	}

	public List<String> getNew_list_service() {
		return new_list_service;
	}

	public int getTotalOldServices() {
		return list_service.size();
	}

	public int getTotalNewServices() {
		return new_list_service.size();
	}
}
