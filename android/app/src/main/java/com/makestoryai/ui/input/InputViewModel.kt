package com.makestoryai.ui.input

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.makestoryai.data.model.GeneratedStory
import com.makestoryai.data.repository.StoryRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class InputViewModel @Inject constructor(
    private val repository: StoryRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<InputUiState>(InputUiState.Initial)
    val uiState: StateFlow<InputUiState> = _uiState.asStateFlow()

    fun generateStory(topic: String, level: String, language: String) {
        viewModelScope.launch {
            _uiState.value = InputUiState.Loading
            
            val result = repository.generateStory(topic, level, language)
            
            result.onSuccess { story ->
                _uiState.value = InputUiState.Success(story)
            }.onFailure { error ->
                _uiState.value = InputUiState.Error(error.message ?: "Unknown error")
            }
        }
    }
    
    fun reset() {
        _uiState.value = InputUiState.Initial
    }
}

sealed class InputUiState {
    object Initial : InputUiState()
    object Loading : InputUiState()
    data class Success(valstory: GeneratedStory) : InputUiState()
    data class Error(val message: String) : InputUiState()
}
