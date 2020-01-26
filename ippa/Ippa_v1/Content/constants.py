BULK_TXN_CREATION_HAS_FAILED = "Bulk transaction has failed."
DASHBOARD_SEGEMENT = "dashboard_content"

#KYC segment
PENDING_KYC_SEGMENT = "pending_kyc_segment"
APPROVED_KYC_SEGMENT = "approved_kyc_segment"
DECLINED_KYC_SEGMENT = "declined_kyc_segment"
PENDING_WITHDRAWL_SEGMENT = "pending_withdrawl_segment"
APPROVED_WITHDRAWL_SEGMENT = "approved_withdrawl_segment"
DECLINED_WITHDRAWL_SEGMENT = "declined_withdrawl_segment"
PENDING_BANK_ACC_INFO_SEGMENT = "pending_ba_segment"
APPROVED_BANK_ACC_INFO_SEGMENT = "approved_ba_segment"
DECLINED_BANK_ACC_INFO_SEGMENT = "declined_ba_segment"

POINTS_SUB_SEGMENT = "points_content"
IMAGES_SUB_SEGMENT = "images_content"
USER_SEGMENT = "user_content"
TRANSACTION_SEGMENT = "transaction_content"

#NAVIGATION BAR STRUCTURE
NAVIGATION_BAR = [
	{
		"segment":"Dashboard",
		"sub_segment":[
			{
				"name":None,
				"content_type":DASHBOARD_SEGEMENT,
				"order":"1",
				"is_default":True,
				"filter_query":{
					"limit":50,
					"offset":0,
					"data_type":"all"
				},
				"tertiary_segment":None
			}
		],
		"order":"1",
		"is_default":True

	},
	{
		"segment":"Approvals",
		"sub_segment":[
			{
				"name":"KYC Verification",
				"content_type":None,
				"order":"1",
				"is_default":True,
				"filter_query":None,
				"tertiary_segment":[
					{
						"name":"Pending",
						"content_type":PENDING_KYC_SEGMENT,
						"order":1,
						"is_default":True,
						"filter_query":{
							"limit":50,
							"offset":0,
							"data_type":"all",
							"query":{
								"kyc_status":"Pending"
							}
						},
					},
					{
						"name":"Approved",
						"content_type":APPROVED_KYC_SEGMENT,
						"order":2,
						"is_default":False,
						"filter_query":{
							"limit":50,
							"offset":0,
							"data_type":"all",
							"query":{
								"kyc_status":"Approved"
							}
						},
					},
					{
						"name":"Declined",
						"content_type":DECLINED_KYC_SEGMENT,
						"order":3,
						"is_default":False,
						"filter_query":{
							"limit":50,
							"offset":0,
							"data_type":"all",
							"query":{
								"kyc_status":"Declined"
							}
						},
					}
				]
			},
			{
				"name":"Withdrawls",
				"content_type":None,
				"order":"2",
				"is_default":False,
				"filter_query":None,
				"tertiary_segment":[
					{
						"name":"Pending",
						"content_type":PENDING_WITHDRAWL_SEGMENT,
						"order":1,
						"is_default":True,
						"filter_query":{
							"limit":50,
							"offset":0,
							"data_type":"all",
							"query":{
								"status":"Pending",
								"txn_type":"Withdraw"
							}
						},
					},
					{
						"name":"Approved",
						"content_type":APPROVED_WITHDRAWL_SEGMENT,
						"order":2,
						"is_default":False,
						"filter_query":{
							"limit":50,
							"offset":0,
							"data_type":"all",
							"query":{
								"status":"Approved",
								"txn_type":"Withdraw"
							}
						},
					},
					{
						"name":"Declined",
						"content_type":DECLINED_WITHDRAWL_SEGMENT,
						"order":3,
						"is_default":False,
						"filter_query":{
							"limit":50,
							"offset":0,
							"data_type":"all",
							"query":{
								"status":"Declined",
								"txn_type":"Withdraw"
							}
						},
					}
				]
			},
			{
				"name":"Bank Info",
				"content_type":None,
				"order":"3",
				"is_default":False,
				"filter_query":None,
				"tertiary_segment":[
					{
						"name":"Pending",
						"content_type":PENDING_BANK_ACC_INFO_SEGMENT,
						"order":1,
						"is_default":True,
						"filter_query":{
							"limit":50,
							"offset":0,
							"data_type":"all",
							"query":{
								"status":"Pending"
							}
						},
					},
					{
						"name":"Approved",
						"content_type":APPROVED_BANK_ACC_INFO_SEGMENT,
						"order":2,
						"is_default":False,
						"filter_query":{
							"limit":50,
							"offset":0,
							"data_type":"all",
							"query":{
								"status":"Approved"
							}
						},
					},
					{
						"name":"Declined",
						"content_type":DECLINED_BANK_ACC_INFO_SEGMENT,
						"order":3,
						"is_default":False,
						"filter_query":{
							"limit":50,
							"offset":0,
							"data_type":"all",
							"query":{
								"status":"Declined"
							}
						},
					}
				]
			},
		],
		"order":"2",
		"is_default":False

	},
	{
		"segment":"Uploads",
		"sub_segment":[
			{
				"name":"Points",
				"content_type":POINTS_SUB_SEGMENT,
				"order":"1",
				"is_default":True,
				"filter_query":{
					"limit":50,
					"offset":0,
					"data_type":"all"
				},
				"tertiary_segment":None
			},
			{
				"name":"Dashboard Images",
				"content_type":IMAGES_SUB_SEGMENT,
				"order":"2",
				"is_default":False,
				"filter_query":{
					"limit":50,
					"offset":0,
					"data_type":"all"
				},
				"tertiary_segment":None
			},

		],
		"order":"3",
		"is_default":False

	},
	{
		"segment":"Users",
		"sub_segment":[
			{
				"name":None,
				"content_type":USER_SEGMENT,
				"order":"1",
				"is_default":True,
				"filter_query":{
					"limit":50,
					"offset":0,
					"data_type":"all"
				},
				"tertiary_segment":None
			}
		],
		"order":"4",
		"is_default":False

	},
	{
		"segment":"Transaction History",
		"sub_segment":[
			{
				"name":None,
				"content_type":TRANSACTION_SEGMENT,
				"order":"1",
				"is_default":True,
				"filter_query":{
					"limit":50,
					"offset":0,
					"data_type":"all"
				},
				"tertiary_segment":None
			}
		],
		"order":"5",
		"is_default":False

	}

]