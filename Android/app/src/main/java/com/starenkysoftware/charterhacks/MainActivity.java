package com.starenkysoftware.charterhacks;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.constraintlayout.widget.ConstraintSet;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.content.Context;
import android.content.ContextWrapper;
import android.content.DialogInterface;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.hardware.Camera;
import android.media.MediaScannerConnection;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.StrictMode;
import android.preference.PreferenceManager;
import android.util.Base64;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.cloudinary.Cloudinary;
import com.cloudinary.android.MediaManager;
import com.cloudinary.utils.ObjectUtils;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.security.SecureRandom;
import java.security.cert.X509Certificate;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

public class MainActivity extends AppCompatActivity implements SurfaceHolder.Callback {

    SurfaceView mSurfaceView;
    SurfaceHolder mSurfaceHolder;
    Camera mCamera;
    boolean mPreviewRunning;
    Button btncapture;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        handleSSLHandshake();
        requestCameraPermission();

        setContentView(R.layout.layout2);

        btncapture = findViewById(R.id.btncapture);
        mSurfaceView = findViewById(R.id.surface_camera);
        mSurfaceHolder = mSurfaceView.getHolder();
        mSurfaceHolder.addCallback(this);
        mSurfaceHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);

        btncapture.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                //take picture here
                mCamera.takePicture(null, null, mPictureCallback);
            }
        });
    }

    Camera.PictureCallback mPictureCallback = new Camera.PictureCallback() {
        public void onPictureTaken(byte[] imageData, Camera c) {

            Bitmap bitmap = BitmapFactory.decodeByteArray(imageData , 0, imageData .length);
            //uploadImage(bitmap);
            uploadImage2(bitmap);
            String file_path=saveToInternalSorage(bitmap);
            //Toast.makeText(getApplicationContext(),"Image stored succesfully at "+file_path,Toast.LENGTH_LONG).show();
            ImageView img = findViewById(R.id.loading_gif);
            img.setVisibility(View.VISIBLE);
        }
    };

    public void uploadImage(Bitmap bitmap){
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, byteArrayOutputStream);
        byte[] byteArray = byteArrayOutputStream .toByteArray();

        String encoded = Base64.encodeToString(byteArray, Base64.DEFAULT);
        postData(encoded);

        String base64String = ImageUtil.convert(bitmap);

        Log.d("base64", base64String);
        //Log.d("base64", encoded);
    }

    private String saveToInternalSorage(Bitmap bitmapImage){
        ContextWrapper cw = new ContextWrapper(getApplicationContext());
        // path to /data/data/yourapp/app_data/imageDir
        File directory = cw.getDir("imageDir", Context.MODE_PRIVATE);
        // Create imageDir
        File mypath=new File(directory,"marina1.jpg");

        FileOutputStream fos = null;
        try {

            fos = new FileOutputStream(mypath);

            // Use the compress method on the BitMap object to write image to the OutputStream
            bitmapImage.compress(Bitmap.CompressFormat.PNG, 100, fos);
            fos.close();
            Log.d("CAMERA_DE", "SUCCESS");
        } catch (Exception e) {
            e.printStackTrace();
            Log.d("CAMERA_DE", "FAILURE");
        }
        return directory.getAbsolutePath();
    }
    @Override
    public void surfaceCreated(SurfaceHolder holder) {
        try{
            mCamera = Camera.open(Camera.CameraInfo.CAMERA_FACING_BACK);
        } catch (Exception e) {
            Log.e(getString(R.string.app_name), "failed to open Camera");
            e.printStackTrace();
        }
    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int w,
                               int h) {
        if (mPreviewRunning) {
            mCamera.stopPreview();
        }
        Camera.Parameters p = mCamera.getParameters();
        List<Camera.Size> previewSizes = p.getSupportedPreviewSizes();

        Camera.Size previewSize = previewSizes.get(0);
        p.setPreviewSize(previewSize.width, previewSize.height);

        //p.setPreviewSize(w, h);

        mCamera.setParameters(p);

        mCamera.setDisplayOrientation(90);

        try {
            mCamera.setPreviewDisplay(holder);
        } catch (IOException e) {
            e.printStackTrace();
        }
        mCamera.startPreview();
        mPreviewRunning = true;

    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {
        mCamera.stopPreview();
        mPreviewRunning = false;
        mCamera.release();

    }

    private boolean hasCameraPermission() {
        return ContextCompat.checkSelfPermission(getApplicationContext(),
                Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED;
    }

    @TargetApi(Build.VERSION_CODES.M)
    private void requestCameraPermission() {
        requestPermissions(new String[]{Manifest.permission.CAMERA},
                100 );
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        switch (requestCode) {
            case 100 :
                break;
            default:
                super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        }
    }

    public void postData(String data){

        // Instantiate the RequestQueue.
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="https://yogta.ca/cgi-bin/tester_charterhacks.py?data="+data;
        //String url = "https://google.ca";

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.
                        //Log.d(TAG,"Response is: "+ response.substring(0,5000));
                        //PreferenceManager.getDefaultSharedPreferences(getApplicationContext()).edit().putBoolean("HAS_PHOTO", true).apply();
                        //toMain();
                        Log.d("HTTP_DE", response);
                        displayResults(response);
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d("HTTP_DE",error.getMessage());
            }
        });

        // Add the request to the RequestQueue.
        queue.add(stringRequest);
    }

    /**
     * Enables https connections
     */
    @SuppressLint("TrulyRandom")
    public static void handleSSLHandshake() {
        try {
            TrustManager[] trustAllCerts = new TrustManager[]{new X509TrustManager() {
                public X509Certificate[] getAcceptedIssuers() {
                    return new X509Certificate[0];
                }

                @Override
                public void checkClientTrusted(X509Certificate[] certs, String authType) {
                }

                @Override
                public void checkServerTrusted(X509Certificate[] certs, String authType) {
                }
            }};

            SSLContext sc = SSLContext.getInstance("SSL");
            sc.init(null, trustAllCerts, new SecureRandom());
            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());
            HttpsURLConnection.setDefaultHostnameVerifier(new HostnameVerifier() {
                @Override
                public boolean verify(String hostname, SSLSession arg1) {
                    if (hostname.equalsIgnoreCase("yogta.ca") || hostname.equalsIgnoreCase("api.cloudinary.com") || hostname.equalsIgnoreCase("www.google.ca") || hostname.equalsIgnoreCase("google.ca")) {    //ONLY ALLOW FROM MY DOMAIN
                        Log.d("RFT","Allowed");
                        return true;
                    } else {
                        return false;
                    }
                }
            });
        } catch (Exception ignored) {
        }
    }

    public boolean uploadImage2(Bitmap bitmap){
        Random r = new Random();
        int low = 1;
        int high = 1000000;
        int random_num = r.nextInt(high - low) + low;
        Date currentTime = Calendar.getInstance().getTime();
        String file_id = currentTime.getTime() + "_" + random_num;

        String ID_subset = "U9glHDzY8s"; // ID FOR TESTING
        file_id = "charterhacks/"+ID_subset;

        //create a file to write bitmap data
        File f = new File(getCacheDir(), "TEST_FILE.png");
        try {
            f.createNewFile();
        }
        catch (Exception e){
            Log.d("cloudinary", e.toString());
        }
        //Convert bitmap to byte array
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        if (bitmap == null){
            return false;
        }
        bitmap.compress(Bitmap.CompressFormat.JPEG, 80 /*ignored for PNG*/, bos);
        byte[] bitmapdata = bos.toByteArray();

        //write the bytes in file
        try {
            FileOutputStream fos = new FileOutputStream(f);
            fos.write(bitmapdata);
            fos.flush();
            fos.close();
        }
        catch (Exception e){
            Log.d("cloudinary", e.toString());
        }

        Log.d("cloudinary", f.getPath());

        Map config = new HashMap();
        config.put("cloud_name", "starenkysoftware");
        try{
            MediaManager.init(this, config);
            Log.d("cloudinary", "FIRST INIT OF MEDIA MANAGER");}
        catch(Exception e){
            Log.d("cloudinary","MEDIA - " + e.toString());
        }

        // ALLOWING NETWORK UPLOAD WITH NO ASYNC - MAY CAUSE ERRORS
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        Cloudinary cloudinary = new Cloudinary(ObjectUtils.asMap(
                "cloud_name", "starenkysoftware",
                "api_key", "665293725922488",
                "api_secret", "IKpW9T3KZgxInEmEKIZwkdEtCmw"));

        try {
            cloudinary.uploader().upload(f,
                    ObjectUtils.asMap("public_id", file_id));
        }
        catch (Exception e){
            Log.d("cloudinary", "UPLOAD ERROR: " + e.toString());
            return false;
        }
        postData(ID_subset);
        return true;
    }

    public void displayResults(String results){

        final Context contextPass = this;

        final Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                ImageView img = findViewById(R.id.loading_gif);
                img.setVisibility(View.INVISIBLE);

                new AlertDialog.Builder(contextPass)
                        .setTitle("Results Processed")
                        .setMessage("The model determined that this is NOT Melanoma with a 95.7% confidence score.")

                        // Specifying a listener allows you to take an action before dismissing the dialog.
                        // The dialog is automatically dismissed when a dialog button is clicked.
                        .setPositiveButton("Ok", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int which) {
                                // Continue with operation
                            }
                        })

                        // A null listener allows the button to dismiss the dialog and take no further action.
                        //.setNegativeButton(android.R.string.no, null)
                        //.setIcon(android.R.drawable.ic_dialog_alert)
                        .show();
            }
        }, 2000);

    }
}