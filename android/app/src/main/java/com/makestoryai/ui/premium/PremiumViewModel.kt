package com.makestoryai.ui.premium

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.makestoryai.data.model.UserStatus
import com.makestoryai.data.repository.StoryRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class PremiumViewModel @Inject constructor(
    private val repository: StoryRepository
) : ViewModel() {

    private val _status = MutableStateFlow<UserStatus?>(null)
    val status: StateFlow<UserStatus?> = _status

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    fun refreshStatus() {
        viewModelScope.launch {
            repository.getUserStatus().onSuccess {
                _status.value = it
            }
        }
    }

    fun buyPremium(onSuccess: () -> Unit) {
        viewModelScope.launch {
            _isLoading.value = true
            repository.buyPremium()
                .onSuccess {
                    _status.value = it
                    onSuccess()
                }
                .onFailure {
                    // Handle error
                }
            _isLoading.value = false
        }
    }
}
