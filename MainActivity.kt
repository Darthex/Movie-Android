package com.example.movierecommendationapplication

import android.app.ProgressDialog
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.DefaultRetryPolicy
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import org.json.JSONObject


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val url = "https://movie-model-android.herokuapp.com"
        val queue = Volley.newRequestQueue(this)
        val intent = Intent(this, MainActivity2::class.java)

        val name1: EditText = findViewById(R.id.editTextTextPersonName)
        val name2: EditText = findViewById(R.id.editTextTextPersonName2)
        val name3: EditText = findViewById(R.id.editTextTextPersonName3)
        val name4: EditText = findViewById(R.id.editTextTextPersonName4)
        val name5: EditText = findViewById(R.id.editTextTextPersonName5)
        val rate1: EditText = findViewById(R.id.editTextNumber)
        val rate2: EditText = findViewById(R.id.editTextNumber2)
        val rate3: EditText = findViewById(R.id.editTextNumber3)
        val rate4: EditText = findViewById(R.id.editTextNumber4)
        val rate5: EditText = findViewById(R.id.editTextNumber5)
        val btn: Button = findViewById(R.id.button)
        val pb:ProgressBar = findViewById(R.id.pb)

        btn.setOnClickListener {
            pb.visibility=View.VISIBLE
            val jsonObj = JSONObject()
            jsonObj.put("movie-name1", name1.text.toString())
            jsonObj.put("movie-name2", name2.text.toString())
            jsonObj.put("movie-name3", name3.text.toString())
            jsonObj.put("movie-name4", name4.text.toString())
            jsonObj.put("movie-name5", name5.text.toString())

            jsonObj.put("rating1", rate1.text.toString())
            jsonObj.put("rating2", rate2.text.toString())
            jsonObj.put("rating3", rate3.text.toString())
            jsonObj.put("rating4", rate4.text.toString())
            jsonObj.put("rating5", rate5.text.toString())


            val jsonRequest = object : JsonObjectRequest(Method.POST, url, jsonObj, {
                Log.d("success", it.toString())
                val img = it.getString("src")
                val name = it.getString("title")
                intent.putExtra("img", img)
                intent.putExtra("name", name)
                startActivity(intent)
                pb.visibility=View.GONE
            }, {
                Log.d("Error", it.toString())
            }){}
            jsonRequest.retryPolicy = (DefaultRetryPolicy(20000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT))
            queue.add(jsonRequest)

        }
    }
}
