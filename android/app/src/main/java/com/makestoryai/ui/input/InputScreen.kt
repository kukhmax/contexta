package com.makestoryai.ui.input

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
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
        
        // Render HTML content
        AndroidView(
            modifier = Modifier.fillMaxWidth(),
            factory = { context ->
                android.widget.TextView(context).apply {
                    textSize = 18f
                    movementMethod = android.text.method.LinkMovementMethod.getInstance()
                }
            },
            update = { textView ->
                textView.text = androidx.core.text.HtmlCompat.fromHtml(
                    story.storyHtml,
                    androidx.core.text.HtmlCompat.FROM_HTML_MODE_LEGACY
                )
            }
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        if (story.audioUrl != null) {
            // Fix URL for emulator if needed (already mostly handled by Retrofit/NetworkModule config for localhost, 
            // but audio URL from backend might be relative e.g. /static/audio/...)
            // If backend returns relative path, we prepend base url.
            // Current backend returns "/static/audio/..."
            val fullAudioUrl = if (story.audioUrl.startsWith("http")) {
                story.audioUrl
            } else {
                "http://10.0.2.2:8000${story.audioUrl}"
            }
            
            com.makestoryai.ui.components.AudioPlayer(audioUrl = fullAudioUrl)
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        Button(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
            Text("Create New Story")
        }
    }
}
