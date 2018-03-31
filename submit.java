import java.sql.Timestamp;
import java.net.*;
import java.net.URL;
import java.net.URLConnection;
import java.net.MalformedURLException;

import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

import java.security.Security;
import java.security.SecureRandom;
import java.security.cert.X509Certificate;
import java.security.cert.CertificateException;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.DataOutputStream;
import java.io.IOException;

import java.util.*;
import java.io.*;

import java.util.zip.GZIPInputStream;

import java.util.zip.GZIPOutputStream;

import java.nio.charset.Charset;
import java.nio.ByteBuffer;

class submit{
	public static void main(String[] args) {
		submit obj=new submit();
		obj.print();		
	}

	void print(){
		try{
			Scanner sc=new Scanner(new FileReader("ptoj.txt"));
			String line=sc.nextLine();
			int pos=line.indexOf("viewform");
			String url=line.substring(0,pos);
			URL loginUrl=new URL(url+"viewform");
		    URL controllerUrl=new URL(url+"formResponse");
		    System.out.println(url+"viewform"+"\n"+url+"formResponse");

		    line=sc.nextLine();
		    ArrayList<String> key=new ArrayList();
		    ArrayList<String> value=new ArrayList();
		    int k=1;
		    while(line.compareTo("#")!=0){
		    	if(k++%2==1){
		    		key.add(line);
		    	}
		    	else{
		    		value.add(line);
		    	}
		    	line=sc.nextLine();
		    }

		    StringBuilder param=new StringBuilder("");
		    for(int i=0;i<key.size()-1;i++){
		    	param.append(key.get(i));
		    	param.append("=");
		    	param.append(value.get(i));
		    	param.append("&");
		    }
		    param.append(key.get(key.size()-1));
		    param.append("=");
		    param.append(value.get(key.size()-1));

		    String parameters=param.toString();

			System.out.println(parameters);
		    HttpCookie cookieValue=null;
		   
		    HttpsURLConnection conn=null;
		    int responseCode=0;
		    DataOutputStream wr=null;

			try{
	            CookieManager manager = new CookieManager();
	            manager.setCookiePolicy(CookiePolicy.ACCEPT_ALL);
	            CookieHandler.setDefault(manager);
	            conn =(HttpsURLConnection) loginUrl.openConnection();
	            conn.getContent();
	            CookieStore cookieJar =  manager.getCookieStore();
	            List <HttpCookie> cookies =cookieJar.getCookies();
	            for (HttpCookie cookie: cookies) {
	        	   cookieValue=cookie;
	        	   System.out.println(cookieValue.getName()+"="+cookieValue.getValue());
	            }
	        } catch(Exception ex) {
	        	ex.printStackTrace();
	           	// return new String[]{"","",""};
	        }
	        System.out.println(cookieValue.getName()+"="+cookieValue.getValue());
	        responseCode = conn.getResponseCode();                                     //CUMPULSORY  
	        System.out.println(responseCode+" 1");
			
			conn=null;

	        conn=(HttpsURLConnection) controllerUrl.openConnection();
	        conn.setRequestMethod("POST");
            conn.setRequestProperty("Accept","text/plain, */*; q=0.01");
            conn.setRequestProperty("Accept-Encoding","gzip, deflate, br");
            conn.setRequestProperty("Accept-Language", "en-US,en;q=0.9,hi;q=0.8,fa;q=0.7");
            conn.setRequestProperty("Connection", "keep-alive");

            conn.setRequestProperty("Content-Length", Integer.toString(parameters.length()));
            conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
		    conn.setRequestProperty("Cookie",cookieValue.getName()+"="+cookieValue.getValue());
            conn.setRequestProperty("Host", "docs.google.com");   
            conn.setRequestProperty("Origin","docs.google.com");
            conn.setRequestProperty("Referer", "docs.google.com"); 
            conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36");
            conn.setRequestProperty("X-Requested-With","XMLHttpRequest");
            
            conn.setDoOutput(true); //to send data to login page
            conn.setDoInput(true);
            wr = new DataOutputStream(conn.getOutputStream());
            wr.writeBytes(parameters);
            wr.flush();
            wr.close();

            responseCode = conn.getResponseCode();                                     //CUMPULSORY
            System.out.println(responseCode+" 2");
            } catch(Exception ex) {
	        	ex.printStackTrace();
	           	// return new String[]{"","",""};
	        }
	}
}
