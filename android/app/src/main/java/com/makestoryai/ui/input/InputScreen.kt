package com.makestoryai.ui.input

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.makestoryai.data.model.GeneratedStory

@Composable
fun InputScreen(
    viewModel: InputViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    
    var topic by remember { mutableStateOf("Daily Life") }
    var level by remember { mutableStateOf("A1") }
    var language by remember { mutableStateOf("en") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        when (val state = uiState) {
            is InputUiState.Initial -> {
                Text(text = "Make Story AI 🚀", style = MaterialTheme.typography.headlineMedium)
                Spacer(modifier = Modifier.height(32.dp))
                
                OutlinedTextField(
                    value = topic,
                    onValueChange = { topic = it },
                    label = { Text("Topic") },
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // Simple Level Selection (Radio or Dropdown could be better, but MVP)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { level = "A1" }, enabled = level != "A1") { Text("A1") }
                    Button(onClick = { level = "A2" }, enabled = level != "A2") { Text("A2") }
                    Button(onClick = { level = "B1" }, enabled = level != "B1") { Text("B1") }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Button(
                    onClick = { viewModel.generateStory(topic, level, language) },
                    modifier = Modifier.fillMaxWidth(),
                    enabled = topic.isNotBlank()
                ) {
                    Text("Generate Story ✨")
                }
            }
            
            is InputUiState.Loading -> {
                CircularProgressIndicator()
                Text("Generating story...", modifier = Modifier.padding(top = 16.dp))
            }
            
            is InputUiState.Success -> {
                StoryView(story = state.story, onBack = { viewModel.reset() })
            }
            
            is InputUiState.Error -> {
                Text("Error: ${state.message}", color = MaterialTheme.colorScheme.error)
                Button(onClick = { viewModel.reset() }) {
                    Text("Try Again")
                }
            }
        }
    }
}

@Composable
fun StoryView(story: GeneratedStory, onBack: () -> Unit) {
    Column(modifier = Modifier.fillMaxSize()) {
        Text(text = story.title, style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(16.dp))
        
        // MVP: Just showing raw HTML/text for now. 
        // In real app we would use AndroidView with WebView or AnnotatedString parsing.
        Text(text = story.storyHtml) 
        
        Spacer(modifier = Modifier.height(16.dp))
        
        if (story.audioUrl != null) {
            Text("Audio available at: ${story.audioUrl}")
            // ExoPlayer integration comes in Phase 4
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        Button(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
            Text("Create New Story")
        }
    }
}
