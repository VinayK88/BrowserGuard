from .models import Extension, Decision

EXTENSIONS=(
Extension('ext-001','Calendar Notes',True,('storage','activeTab'),0,'stable',420,83,False,False,False,False,False,110,100,Decision.NORMAL),
Extension('ext-002','AI Page Helper',False,('tabs','storage','cookies','scripting','<all_urls>'),3,'external',14,612,True,True,True,True,True,8800,120,Decision.CRITICAL),
Extension('ext-003','Sales Capture',True,('tabs','storage','webRequest'),1,'stable',800,190,True,False,False,True,True,950,280,Decision.HIGH_RISK),
Extension('ext-004','Legacy Clipboard Pro',False,('clipboardRead','clipboardWrite','tabs','<all_urls>'),0,'stable',1700,71,False,False,False,False,False,80,90,Decision.HIGH_RISK),
Extension('ext-005','Meeting Summarizer',True,('tabs','storage','identity'),0,'stable',200,244,True,False,True,False,True,360,240,Decision.REVIEW),
Extension('ext-006','PDF Toolkit',True,('downloads','storage'),0,'stable',900,120,False,False,False,False,False,125,130,Decision.NORMAL),
Extension('ext-007','Coupon Companion',False,('tabs','cookies','webRequest','<all_urls>'),2,'external',20,330,True,True,False,True,False,4200,180,Decision.CRITICAL),
Extension('ext-008','Dev Header Switcher',False,('webRequest','webRequestBlocking','tabs'),1,'beta',120,48,True,False,False,False,False,340,150,Decision.HIGH_RISK),
)
