package com.makestoryai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Create
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.runtime.*
import com.makestoryai.ui.input.InputScreen
import com.makestoryai.ui.history.HistoryScreen
import com.makestoryai.ui.premium.PremiumScreen
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    MainScreen()
                }
            }
        }
    }
}

@Composable
fun MainScreen() {
    var currentScreen by remember { mutableStateOf(Screen.Input) }
    var selectedStory by remember { mutableStateOf<com.makestoryai.data.model.GeneratedStory?>(null) }

    Scaffold(
        bottomBar = {
            if (selectedStory == null) { // Hide bottom bar when reading story
                NavigationBar {
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Create, contentDescription = "Create") },
                        label = { Text("Create") },
                        selected = currentScreen == Screen.Input,
                        onClick = { currentScreen = Screen.Input }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.List, contentDescription = "History") },
                        label = { Text("History") },
                        selected = currentScreen == Screen.History,
                        onClick = { currentScreen = Screen.History }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Star, contentDescription = "Premium") },
                        label = { Text("Premium") },
                        selected = currentScreen == Screen.Premium,
                        onClick = { currentScreen = Screen.Premium }
                    )
                }
            }
        }
    ) { innerPadding ->
        Box(modifier = Modifier.padding(innerPadding)) {
            if (selectedStory != null) {
               com.makestoryai.ui.input.StoryView(
                   story = selectedStory!!, 
                   onBack = { selectedStory = null }
               )
            } else {
                when (currentScreen) {
                    Screen.Input -> com.makestoryai.ui.input.InputScreen()
                    Screen.History -> com.makestoryai.ui.history.HistoryScreen(
                        onStoryClick = { story -> selectedStory = story }
                    )
                    Screen.Premium -> com.makestoryai.ui.premium.PremiumScreen(
                        onPurchaseSuccess = { /* Celebrate? */ }
                    )
                }
            }
        }
    }
}

enum class Screen {
    Input, History, Premium
}


