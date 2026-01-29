package com.makestoryai.data.api

import com.makestoryai.data.model.GeneratedStory
import com.makestoryai.data.model.StoryRequest
import retrofit2.http.Body
import retrofit2.http.POST

interface StoryApi {
    @POST("api/v1/generate")
    suspend fun generateStory(
        @retrofit2.http.Header("x-device-id") deviceId: String,
        @Body request: StoryRequest
    ): GeneratedStory

    @retrofit2.http.GET("api/v1/user/status")
    suspend fun getUserStatus(
        @retrofit2.http.Header("x-device-id") deviceId: String
    ): com.makestoryai.data.model.UserStatus

    @POST("api/v1/user/upgrade")
    suspend fun upgradeUser(@Body request: com.makestoryai.data.model.PurchaseRequest): com.makestoryai.data.model.UserStatus
}
