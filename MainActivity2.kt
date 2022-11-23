package com.example.movierecommendationapplication

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import com.bumptech.glide.Glide

class MainActivity2 : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main2)

        val txtV:TextView = findViewById(R.id.moviename)
        val imgV:ImageView = findViewById(R.id.img)

        val name = intent.getStringExtra("name")
        val image = intent.getStringExtra("img")

        txtV.text = name.toString()
        Glide.with(this).load(image).into(imgV)

    }
}
