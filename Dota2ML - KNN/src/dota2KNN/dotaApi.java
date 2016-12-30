package dota2KNN;

import java.io.IOException;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

public class dotaApi {

	private String matchid;

	public dotaApi(String matchid) {
		super();
		this.matchid = matchid;
	}

	public String getMatchid() {
		return matchid;
	}

	public void setMatchid(String matchid) {
		this.matchid = matchid;
	}

public String connectApi()
{
	String html="";  
	
	 
	 
	 CloseableHttpClient httpclient = HttpClients.createDefault();  
	    HttpGet httpGet = new HttpGet("http://api.opendota.com/api/matches/"+matchid);        httpGet.setHeader("Accept", "text/html, */*; q=0.01");  
	    httpGet.setHeader("Accept-Encoding", "gzip, deflate,sdch");  
	    httpGet.setHeader("Accept-Language", "zh-CN,zh;q=0.8");  
	    httpGet.setHeader("Connection", "keep-alive");  
	    httpGet.setHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36)");  
	    try {  
	        CloseableHttpResponse response = httpclient.execute(httpGet);             
	       
	        html = EntityUtils.toString(response.getEntity(), "utf-8");  
	    } catch (IOException e) {  
	        System.out.println("----------Connection timeout--------");  
	    }  
	    return html;
	
	
}
	

}
