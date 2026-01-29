package com.makestoryai.data.model

import com.google.gson.annotations.SerializedName

data class UserStatus(
    @SerializedName("device_id") val deviceId: String,
    @SerializedName("is_premium") val isPremium: Boolean,
    @SerializedName("daily_count") val dailyCount: Int,
    @SerializedName("limit") val limit: Int
)

data class PurchaseRequest(
    @SerializedName("device_id") val deviceId: String
)
