package dota2KNN;

import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONObject;

import dota2KNN.dotaApi;
import net.sf.javaml.core.Dataset;
import net.sf.javaml.core.DefaultDataset;
import net.sf.javaml.core.DenseInstance;

public class Preprocessor {
	private ArrayList<Dataset> data;
	private Dataset testdata;


	public Preprocessor() {
		data = new ArrayList<>();
		testdata = new DefaultDataset();
	}

	public void grab(String a, String username, String password, int num, int testnum) throws InterruptedException {
		
		PreparedStatement stmt = null;
		int counter = 0;
	 Dataset datacontainer = new DefaultDataset();
		ArrayList<ArrayList<String>> matches = new ArrayList<>();

		ResultSet rs = null;
		try {
			Connection con = DriverManager.getConnection(a, username, password);
			String sql = "select * from detail_match";
			stmt = con.prepareStatement(sql);
			rs = stmt.executeQuery();
			while (rs.next()) {
				
				
				ArrayList<String> match = new ArrayList<>();
				match.add(rs.getInt("player1Hero")+"");
				match.add(rs.getInt("player2Hero")+"");
				match.add(rs.getInt("player3Hero")+"");
				match.add(rs.getInt("player4Hero")+"");
				match.add(rs.getInt("player5Hero")+"");
				match.add(rs.getInt("player6Hero")+"");
				match.add(rs.getInt("player7Hero")+"");
				match.add(rs.getInt("player8Hero")+"");
				match.add(rs.getInt("player9Hero")+"");
				match.add(rs.getInt("player10Hero")+"");
				match.add(rs.getInt("rad_win")+"");
				matches.add(match);
				counter++;
				System.out.println(counter);
				if (counter >= num+testnum)
					break;
				
			}
		
		} catch (SQLException se) {
			System.out.println("connecting fail");
			se.printStackTrace();
		}
		counter = 0;
		for ( ArrayList<String> match : matches) {
			double[] instance1 = new double[228];
			double[] instance2 = new double[228];
			boolean isRadwin = match.get(match.size()-1).equals( "1");
				for (int i = 0; i < match.size()-1; i++) {
					int heroid = Integer.parseInt(match.get(i));
	
					if(heroid<=0)
						break;
					
					if (i<5) {
						instance1[heroid] = 1;
						instance2[heroid + 114] = 1;
					} else {
						instance1[heroid + 114] = 1;
						instance2[heroid ] = 1;
					}
				}
				String aa = isRadwin == true ? "win" : "not win";
				String b = isRadwin != true ? "win" : "not win";
				if(counter<num)
				{
				datacontainer.add(new DenseInstance(instance1, aa));
				datacontainer.add(new DenseInstance(instance2, b));
				if(counter%500 == 0) data.add(datacontainer.copy());
				}
				if(counter >= num)
				{
					testdata.add(new DenseInstance(instance1,aa));
				testdata.add(new DenseInstance(instance2,b));
				}
				System.out.println(counter++);
		}	

	}
public void gra(String a, String username, String password, int num, int testnum) throws InterruptedException {
		
		PreparedStatement stmt = null;
		int counter = 0;

		ArrayList<ArrayList<String>> matches = new ArrayList<>();

		ResultSet rs = null;
		try {
			Connection con = DriverManager.getConnection(a, username, password);
			String sql = "select * from tour_match";
			stmt = con.prepareStatement(sql);
			rs = stmt.executeQuery();
			while (rs.next()) {
				
				int a1 = rs.getInt("pick_1");
				ArrayList<String> match = new ArrayList<>();
				if(a1 == 0) 
					continue;
				
//				Timestamp filter = rs.getTimestamp("match_time");
//				int yea = Integer.valueOf(filter.toString().substring(0,4));
//				if(yea<2014) continue;

				match.add(rs.getInt("pick_1")+"");
				match.add(rs.getInt("pick_4")+"");
				match.add(rs.getInt("pick_6")+"");
				match.add(rs.getInt("pick_8")+"");
				match.add(rs.getInt("pick_9")+"");
				match.add(rs.getInt("pick_2")+"");
				match.add(rs.getInt("pick_3")+"");
				match.add(rs.getInt("pick_5")+"");
				match.add(rs.getInt("pick_7")+"");
				match.add(rs.getInt("pick_10")+"");
				match.add(rs.getInt("rad_win")+"");
				match.add(rs.getInt("first_pick_team")+"");
				matches.add(match);
				counter++;
				System.out.println(counter);
				if (counter >= num+testnum)
					break;
				
			}
		
		} catch (SQLException se) {
			System.out.println("connecting fail");
			se.printStackTrace();
		}
		counter = 0;
		for ( ArrayList<String> match : matches) {
			double[] instance1 = new double[228];
			double[] instance2 = new double[228];
			boolean isRadwin = match.get(match.size()-2).equals( "1");
			boolean isRadfirst = match.get(match.size()-1).equals("0");
				for (int i = 0; i < match.size()-2; i++) {
					int heroid = Integer.parseInt(match.get(i));
	
					if(heroid<=0)
						break;
					if(!isRadfirst)
					if (i>=5) {
						instance1[heroid] = 1;
						instance2[heroid + 114] = 1;
					} else {
						instance1[heroid + 114] = 1;
						instance2[heroid ] = 1;
					}
					else
						if (i<5) {
							instance1[heroid] = 1;
							instance2[heroid + 114] = 1;
						} else {
							instance1[heroid + 114] = 1;
							instance2[heroid ] = 1;
						}
				}
				String aa = isRadwin == true ? "win" : "not win";
				String b = isRadwin != true ? "win" : "not win";
				if(counter<num)
				{
				//data.add(new DenseInstance(instance1, aa));
				//data.add(new DenseInstance(instance2, b));
				}
				if(counter >= num)
				{
					testdata.add(new DenseInstance(instance1,aa));
				testdata.add(new DenseInstance(instance2,b));
				}
				System.out.println(counter++);
		}	

	}
	public void grabseq(String a, String username, String password, int num, int testnum) throws InterruptedException {
		PreparedStatement stmt = null;
		int counter = 0;

		ArrayList<ArrayList<String>> matches = new ArrayList<>();

		ResultSet rs = null;
		try {
			Connection con = DriverManager.getConnection(a, username, password);
			String sql = "select * from detail_match";
			stmt = con.prepareStatement(sql);
			rs = stmt.executeQuery();
			while (rs.next()) {
				
				
				ArrayList<String> match = new ArrayList<>();
				match.add(rs.getInt("player1Hero")+" "+rs.getInt("player1Seq"));
				match.add(rs.getInt("player2Hero")+" "+rs.getInt("player2Seq"));
				match.add(rs.getInt("player3Hero")+ " "+rs.getInt("player3Seq"));
				match.add(rs.getInt("player4Hero")+ " "+rs.getInt("player4Seq"));
				match.add(rs.getInt("player5Hero")+ " "+rs.getInt("player5Seq"));
				match.add(rs.getInt("player6Hero")+ " "+rs.getInt("player6Seq"));
				match.add(rs.getInt("player7Hero")+ " "+rs.getInt("player7Seq"));
				match.add(rs.getInt("player8Hero")+ " "+rs.getInt("player8Seq"));
				match.add(rs.getInt("player9Hero")+ " "+rs.getInt("player9Seq"));
				match.add(rs.getInt("player10Hero")+ " "+rs.getInt("player10Seq"));
				match.add(rs.getInt("rad_win")+"");
				matches.add(match);
				counter++;
				System.out.println(counter);
				if (counter >= num+testnum)
					break;
				
			}
		
		} catch (SQLException se) {
			System.out.println("connecting fail");
			se.printStackTrace();
		}
		counter = 0;
		for ( ArrayList<String> match : matches) {
			double[] instance1 = new double[228*10];
			double[] instance2 = new double[228*10];
			boolean isRadwin = match.get(match.size()-1).equals( "1");
				for (int i = 0; i < match.size()-1; i++) {
					int heroid = Integer.parseInt(match.get(i).split(" ")[0]);
					int heroseq = Integer.parseInt(match.get(i).split(" ")[1])-1;
					if(heroseq>9||heroid<=0)
						break;
					
					if (i<5) {
						instance1[heroid+114*heroseq ] = 1;
						instance2[heroid  + 114*heroseq+114*10] = 1;
					} else {
						instance1[heroid  + 114*heroseq+114*10] = 1;
						instance2[heroid +114*heroseq] = 1;
					}
				}
				String aa = isRadwin == true ? "win" : "not win";
				String b = isRadwin != true ? "win" : "not win";
				if(counter<=num)
				{
				//data.add(new DenseInstance(instance1, aa));
				//data.add(new DenseInstance(instance2, b));
				}
				if(counter > num)
				{
					testdata.add(new DenseInstance(instance1,aa));
				testdata.add(new DenseInstance(instance2,b));
				}
				System.out.println(counter++);
		}	

	}

	public Dataset getTestdata() {
		return testdata;
	}

	public void setTestdata(Dataset testdata) {
		this.testdata = testdata;
	}

	public ArrayList<Dataset> getData() {
		return data;
	}

	public void setData(ArrayList<Dataset> data) {
		this.data = data;
	}
}
