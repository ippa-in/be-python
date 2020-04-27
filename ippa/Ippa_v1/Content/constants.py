BULK_TXN_CREATION_HAS_FAILED = "Bulk transaction has failed."
DASHBOARD_SEGEMENT = "dashboard_content"

#KYC segment
PENDING_KYC_SEGMENT = "pending_kyc_segment"
APPROVED_KYC_SEGMENT = "approved_kyc_segment"
DECLINED_KYC_SEGMENT = "declined_kyc_segment"
PENDING_WITHDRAWL_SEGMENT = "pending_withdraw_segment"
APPROVED_WITHDRAWL_SEGMENT = "approved_withdraw_segment"
DECLINED_WITHDRAWL_SEGMENT = "declined_withdraw_segment"
PENDING_BANK_ACC_INFO_SEGMENT = "pending_ba_segment"
APPROVED_BANK_ACC_INFO_SEGMENT = "approved_ba_segment"
DECLINED_BANK_ACC_INFO_SEGMENT = "declined_ba_segment"

POINTS_SUB_SEGMENT = "points_content"
IMAGES_SUB_SEGMENT = "images_content"
AD_SUB_SEGMENT = "ads_content"
USER_SEGMENT = "user_content"
TRANSACTION_SEGMENT = "transaction_content"
REWARD_SEGMENT = "reward_content"

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
				"sort_key":[],
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
				"sort_key":[],
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
						"sort_key":[]
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
						"sort_key":[],
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
						"sort_key":[],
					}
				]
			},
			{
				"name":"Withdrawals",
				"content_type":None,
				"order":"2",
				"is_default":False,
				"filter_query":None,
				"sort_key":[],
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
						"sort_key":[],
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
						"sort_key":[],
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
						"sort_key":[],
					}
				]
			},
			{
				"name":"Bank Info",
				"content_type":None,
				"order":"3",
				"is_default":False,
				"filter_query":None,
				"sort_key":[],
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
						"sort_key":[],
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
						"sort_key":[],
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
						"sort_key":[],
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
				"sort_key":["-created_on"],
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
				"sort_key":["order"],
				"tertiary_segment":None
			},
			{
				"name":"Advertisements",
				"content_type":AD_SUB_SEGMENT,
				"order":"3",
				"is_default":False,
				"filter_query":{
					"limit":50,
					"offset":0,
					"data_type":"all"
				},
				"sort_key":["order"],
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
				"sort_key":[],
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
				"sort_key":[],
				"tertiary_segment":None
			}
		],
		"order":"5",
		"is_default":False

	},
	{
		"segment":"Reward Uploads",
		"sub_segment":[
			{
				"name":None,
				"content_type":REWARD_SEGMENT,
				"order":"1",
				"is_default":True,
				"filter_query":{
					"limit":50,
					"offset":0,
					"data_type":"all"
				},
				"sort_key":[],
				"tertiary_segment":None
			}
		],
		"order":"6",
		"is_default":False

	},

]

#Mapping of columns and keys how to get from filter data

CONTENT_COLUMN_MAPPING = {
	PENDING_KYC_SEGMENT:[
		{
			"display_name":"Date",
			"lookup_key":"date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"User name",
			"lookup_key":"user_name",
			"key_type":"link",
			"order":2
		},
		{
			"display_name":"Status",
			"lookup_key":"kyc_status",
			"key_type":"status",
			"order":3
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Phone",
			"lookup_key":"mobile_number",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Attachement",
			"lookup_key":"kyc_images",
			"key_type":"list",
			"order":6
		},
		{
			"display_name":"",
			"lookup_key":"player_id",
			"key_type":"action",
			"order":7
		}
	],
	APPROVED_KYC_SEGMENT:[
		{
			"display_name":"Date",
			"lookup_key":"date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"User name",
			"lookup_key":"user_name",
			"key_type":"link",
			"order":2
		},
		{
			"display_name":"Status",
			"lookup_key":"kyc_status",
			"key_type":"status",
			"order":3
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Phone",
			"lookup_key":"mobile_number",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Attachement",
			"lookup_key":"kyc_images",
			"key_type":"list",
			"order":6
		},
		{
			"display_name":"",
			"lookup_key":"player_id",
			"key_type":"action",
			"order":7
		}
	],
	DECLINED_KYC_SEGMENT:[
		{
			"display_name":"Date",
			"lookup_key":"date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"User name",
			"lookup_key":"user_name",
			"key_type":"link",
			"order":2
		},
		{
			"display_name":"Status",
			"lookup_key":"kyc_status",
			"key_type":"status",
			"order":3
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Phone",
			"lookup_key":"mobile_number",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Attachement",
			"lookup_key":"kyc_images",
			"key_type":"list",
			"order":6
		},
		{
			"display_name":"",
			"lookup_key":"player_id",
			"key_type":"action",
			"order":7
		}
	],
	PENDING_WITHDRAWL_SEGMENT:[
		{
			"display_name":"Date",
			"lookup_key":"date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"User name",
			"lookup_key":"user.user_name",
			"key_type":"link",
			"order":2
		},
		{
			"display_name":"Status",
			"lookup_key":"kyc_status",
			"key_type":"status",
			"order":3
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Phone",
			"lookup_key":"mobile_number",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Bank Info",
			"lookup_key":"acc_number",
			"key_type":"link",
			"order":6
		},
		{
			"display_name":"",
			"lookup_key":"txn_id",
			"key_type":"action",
			"order":7
		}
	],
	APPROVED_WITHDRAWL_SEGMENT:[
		{
			"display_name":"Date",
			"lookup_key":"date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"User name",
			"lookup_key":"user.user_name",
			"key_type":"link",
			"order":2
		},
		{
			"display_name":"Status",
			"lookup_key":"kyc_status",
			"key_type":"status",
			"order":3
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Phone",
			"lookup_key":"mobile_number",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Bank Info",
			"lookup_key":"acc_number",
			"key_type":"link",
			"order":6
		},
		{
			"display_name":"",
			"lookup_key":"txn_id",
			"key_type":"action",
			"order":7
		}
	],
	DECLINED_WITHDRAWL_SEGMENT:[
		{
			"display_name":"Date",
			"lookup_key":"date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"User name",
			"lookup_key":"user.user_name",
			"key_type":"link",
			"order":2
		},
		{
			"display_name":"Status",
			"lookup_key":"kyc_status",
			"key_type":"status",
			"order":3
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Phone",
			"lookup_key":"mobile_number",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Bank Info",
			"lookup_key":"acc_number",
			"key_type":"link",
			"order":6
		},
		{
			"display_name":"",
			"lookup_key":"txn_id",
			"key_type":"action",
			"order":7
		}
	],
	PENDING_BANK_ACC_INFO_SEGMENT:[
		{
			"display_name":"Date",
			"lookup_key":"date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"User name",
			"lookup_key":"user.user_name",
			"key_type":"link",
			"order":2
		},
		{
			"display_name":"Status",
			"lookup_key":"kyc_status",
			"key_type":"status",
			"order":3
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Phone",
			"lookup_key":"mobile_number",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Bank Info",
			"lookup_key":"acc_number",
			"key_type":"link",
			"order":6
		},
		{
			"display_name":"",
			"lookup_key":"acc_id",
			"key_type":"action",
			"order":7
		}
	],
	APPROVED_BANK_ACC_INFO_SEGMENT:[
		{
			"display_name":"Date",
			"lookup_key":"date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"User name",
			"lookup_key":"user.user_name",
			"key_type":"link",
			"order":2
		},
		{
			"display_name":"Status",
			"lookup_key":"kyc_status",
			"key_type":"status",
			"order":3
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Phone",
			"lookup_key":"mobile_number",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Bank Info",
			"lookup_key":"acc_number",
			"key_type":"link",
			"order":6
		},
		{
			"display_name":"",
			"lookup_key":"acc_id",
			"key_type":"action",
			"order":7
		}
	],
	DECLINED_BANK_ACC_INFO_SEGMENT:[
		{
			"display_name":"Date",
			"lookup_key":"date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"User name",
			"lookup_key":"user.user_name",
			"key_type":"link",
			"order":2
		},
		{
			"display_name":"Status",
			"lookup_key":"kyc_status",
			"key_type":"status",
			"order":3
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Phone",
			"lookup_key":"mobile_number",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Bank Info",
			"lookup_key":"acc_number",
			"key_type":"link",
			"order":6
		},
		{
			"display_name":"",
			"lookup_key":"acc_id",
			"key_type":"action",
			"order":7
		}
	],
	USER_SEGMENT:[
		{
			"display_name":"User name",
			"lookup_key":"user_name",
			"key_type":"string",
			"order":1
		},
		{
			"display_name":"KYC status",
			"lookup_key":"kyc_status",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"string",
			"order":2
		},
		{
			"display_name":"Total points",
			"lookup_key":"points.total_points",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Phone",
			"lookup_key":"mobile_number",
			"key_type":"string",
			"order":3
		},
		{
			"display_name":"Bank status",
			"lookup_key":"bank_acc_status",
			"key_type":"string",
			"order":6
		},
		{
			"display_name":"Email status",
			"lookup_key":"is_email_verified",
			"key_type":"string",
			"order":7
		},
	],
	TRANSACTION_SEGMENT:[
		{
			"display_name":"Date",
			"lookup_key":"date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"User name",
			"lookup_key":"user.user_name",
			"key_type":"link",
			"order":2
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"string",
			"order":3
		},
		{
			"display_name":"Transaction type",
			"lookup_key":"txn_type",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Network",
			"lookup_key":"network.name",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Points",
			"lookup_key":"amount",
			"key_type":"string",
			"order":6
		}
	],
	POINTS_SUB_SEGMENT:[
		{
			"display_name":"Date",
			"lookup_key":"Date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"User name",
			"lookup_key":"UserName",
			"key_type":"string",
			"order":2
		},
		{
			"display_name":"Email",
			"lookup_key":"email_id",
			"key_type":"Email",
			"order":3
		},
		{
			"display_name":"Transaction type",
			"lookup_key":"Transaction Type",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Network",
			"lookup_key":"Network",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Points",
			"lookup_key":"Amount",
			"key_type":"string",
			"order":6
		}
	],
	REWARD_SEGMENT:[
		{
			"display_name":"From Date",
			"lookup_key":"from_date",
			"key_type":"date",
			"order":1
		},
		{
			"display_name":"To Date",
			"lookup_key":"to_date",
			"key_type":"date",
			"order":2
		},
		{
			"display_name":"Title",
			"lookup_key":"title",
			"key_type":"string",
			"order":3
		},
		{
			"display_name":"Network",
			"lookup_key":"network.name",
			"key_type":"string",
			"order":4
		},
		{
			"display_name":"Name of Points",
			"lookup_key":"points_name",
			"key_type":"string",
			"order":5
		},
		{
			"display_name":"Goal Points",
			"lookup_key":"goal_points",
			"key_type":"string",
			"order":6
		},

	],
}