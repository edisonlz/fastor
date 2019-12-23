# -*- coding: utf-8 -*-
"""
    beecloud.entity
    ~~~~~~~~~
    This module contains data entity.
    :created by xuanzhui on 2015/12/24.
    :copyright (c) 2015 BeeCloud.
    :license: MIT, see LICENSE for more details.
"""

import sys


# integer-long compatibility
if sys.version_info > (3, 0):
    long = int


class BCApp:
    """
    correspond to console app
    """
    def __init__(self):
        self.app_id = None
        self.app_secret = None
        self.test_secret = None
        self.master_secret = None
        self.is_test_mode = False
        # If you specify a single value for the timeout(seconds), the timeout value will be applied to both
        # the connect and the read timeouts. Specify a tuple if you would like to set the values separately.
        # If the remote server is very slow, you can tell Requests to wait forever for a response,
        # by passing None as a timeout value and then retrieving a cup of coffee.
        self.timeout = None  # (10, 60)


class BCChannelType:
    WX = 'WX'
    WX_APP = 'WX_APP'
    WX_NATIVE = 'WX_NATIVE'
    WX_SCAN = 'WX_SCAN'
    WX_JSAPI = 'WX_JSAPI'
    WX_REDPACK = 'WX_REDPACK'
    WX_TRANSFER = 'WX_TRANSFER'

    ALI = 'ALI'
    ALI_APP = 'ALI_APP'
    ALI_WEB = 'ALI_WEB'
    ALI_WAP = 'ALI_WAP'
    ALI_QRCODE = 'ALI_QRCODE'
    ALI_OFFLINE_QRCODE = 'ALI_OFFLINE_QRCODE'
    ALI_SCAN  = 'ALI_SCAN'
    ALI_TRANSFER = 'ALI_TRANSFER'

    UN = 'UN'
    UN_APP = 'UN_APP'
    UN_WEB = 'UN_WEB'
    UN_WAP = 'UN_WAP'

    JD = 'JD'
    JD_WAP = 'JD_WAP'
    JD_WEB = 'JD_WEB'

    YEE = 'YEE'
    YEE_WAP = 'YEE_WAP'
    YEE_WEB = 'YEE_WEB'
    YEE_NOBANKCARD = 'YEE_NOBANKCARD'

    KUAIQIAN = 'KUAIQIAN'
    KUAIQIAN_WEB = 'KUAIQIAN_WEB'

    PAYPAL = 'PAYPAL'
    # 生产环境支付，用于手机APP
    PAYPAL_LIVE = 'PAYPAL_LIVE'
    # 沙箱环境支付，用于手机APP
    PAYPAL_SANDBOX = 'PAYPAL_SANDBOX'
    # 以下用于PC
    # 跳转到paypal使用paypal内支付
    PAYPAL_PAYPAL = 'PAYPAL_PAYPAL'
    # 直接使用信用卡支付（paypal渠道）
    PAYPAL_CREDITCARD = 'PAYPAL_CREDITCARD'
    # 使用存储的行用卡id支付（信用卡信息存储在PAYPAL）
    PAYPAL_SAVED_CREDITCARD = 'PAYPAL_SAVED_CREDITCARD'

    BD = 'BD'
    BD_APP = 'BD_APP'
    BD_WAP = 'BD_WAP'
    BD_WEB = 'BD_WEB'

    BC = 'BC'
    BC_GATEWAY = 'BC_GATEWAY'
    BC_APP = 'BC_APP'
    BC_EXPRESS = 'BC_EXPRESS'
    BC_TRANSFER = 'BC_TRANSFER'
    BC_NATIVE = 'BC_NATIVE'
    BC_WX_WAP = 'BC_WX_WAP'
    BC_ALI_QRCODE = 'BC_ALI_QRCODE'
    BC_ALI_SCAN = 'BC_ALI_SCAN'
    BC_WX_SCAN = 'BC_WX_SCAN'


class BCReqType:
    PAY = 0
    QUERY = 1
    REFUND = 2
    TRANSFER = 4


class BCPayReqParams:
    def __init__(self):
        # 渠道类型
        self.channel = None

        # 订单总金额
        self.total_fee = None

        # 商户订单号
        self.bill_no = None

        # 订单标题
        self.title = None

        # 附加数据
        self.optional = None

        # 商家用户ID，如果传入可以在控制台查看用户行为
        self.buyer_id = None

        # 卡券ID，用于营销
        self.coupon_id = None

        # 分析数据
        self.analysis = None

        # 同步返回页面
        self.return_url = None

        # 订单失效时间
        self.bill_timeout = None


class BCRefundReqParams:
    def __init__(self):
        # 渠道类型
        self.channel = None

        # 商户退款单号
        self.refund_no = None

        # 商户订单号
        self.bill_no = None

        # 退款金额
        self.refund_fee = None

        # 附加数据
        self.optional = None

        # 是否为预退款
        self.need_approval = None


class BCPreRefundAuditParams:
    def __init__(self):
        # 渠道类型
        self.channel = None

        # 预退款记录id列表
        self.ids = None

        # 同意或者驳回
        self.agree = None

        # 驳回理由
        self.deny_reason = None


class BCQueryReqParams:
    def __init__(self):
        # 渠道类型
        self.channel = None

        # 商户订单号
        self.bill_no = None

        # 商户退款单号
        # 仅对查询退款有效
        self.refund_no = None

        # 订单是否成功
        # 仅对支付查询有效
        self.spay_result = None

        # 标识退款记录是否为预退款
        # 仅对查询退款有效
        self.need_approval = None

        # 是否需要返回渠道详细信息
        self.need_detail = None

        # 起始时间
        self.start_time = None

        # 结束时间
        self.end_time = None

        # 查询起始位置
        self.skip = None

        # 查询的条数
        self.limit = None


# 不可用于订单和退款的查询！！！
class BCQueryCriteria:
    def __init__(self):
        # query objects created before or equal to the given UNIX timestamp in ms
        self.created_before = None

        # query objects created after or equal to the given UNIX timestamp in ms
        self.created_after = None

        # If count_only is true, only the total count of all objects that match your filters will be returned
        self.count_only = None

        # skip some objects for pagination
        self.skip = None

        # limit the number of objects
        self.limit = None


class BCResult:
    def __init__(self):
        self.result_code = None
        self.result_msg = None
        self.err_detail = None


class BCBill:
    def __init__(self):
        # 订单记录的唯一标识
        self.id = None

        # 订单号
        self.bill_no = None

        self.channel = None

        # 子渠道
        self.sub_channel = None

        # 渠道交易号，当支付成功时有值
        self.trade_no = None

        # 订单创建时间，毫秒时间戳，13位
        self.create_time = None

        # 附加数据
        self.optional = None

        # 订单是否成功
        self.spay_result = None

        # 商品标题
        self.title = None

        # 实付金额，单位为分
        self.total_fee = None

        # 订单金额，单位为分
        self.bill_fee = None

        # 优惠金额，单位为分
        self.discount = None

        # 卡券ID，可能为空
        self.coupon_id = None

        # 渠道详细信息
        self.message_detail = None

        # 订单是否已经撤销
        self.revert_result = None

        # 订单是否已经退款
        self.refund_result = None


class BCRefund:
    def __init__(self):
        # 退款记录的唯一标识
        self.id = None

        # 支付订单号
        self.bill_no = None

        self.channel = None

        # 子渠道
        self.sub_channel = None

        # 退款是否完成
        self.finish = None

        # 退款创建时间
        self.create_time = None

        # 附加数据
        self.optional = None

        # 退款是否成功
        self.result = None

        # 商品标题
        self.title = None

        # 订单金额，单位为分
        self.total_fee = None

        # 退款金额，单位为分
        self.refund_fee = None

        # 退款单号
        self.refund_no = None

        # 渠道详细信息
        self.message_detail = None


class BCTransferReqParams:
    def __init__(self):
        # 渠道类型 WX_REDPACK, WX_TRANSFER, ALI_TRANSFER
        self.channel = None

        # 打款单号
        self.transfer_no = None

        # 打款金额
        self.total_fee = None

        # 打款说明
        self.desc = None

        # 支付渠道方内收款人的标示，微信为openid，支付宝为支付宝账户
        self.channel_user_id = None

        # 支付渠道内收款人账户名， 支付宝必填
        self.channel_user_name = None

        # 微信红包的详细描述，Map类型，微信红包必填
        self.redpack_info = None

        # 打款方账号名全称，支付宝必填
        self.account_name = None


class BCTransferRedPack:
    def __init__(self):
        # 红包发送者名称
        self.send_name = None

        # 红包祝福语
        self.wishing = None

        # 红包活动名称
        self.act_name = None


# 用于bc_transfer
class BCCardTransferParams:
    def __init__(self):
        # 下发订单总金额，正整数
        self.total_fee = None

        # 商户订单号
        self.bill_no = None

        # 下发订单标题
        self.title = None

        # 交易源
        self.trade_source = 'OUT_PC'

        # 银行全名
        self.bank_fullname = None

        # 银行卡类型，DE代表借记卡，CR代表信用卡
        self.card_type = None

        # 收款帐户类型
        self.account_type = None

        # 收款帐户号
        self.account_no = None

        # 收款帐户名称
        self.account_name = None

        # 银行绑定的手机号
        self.mobile = None

        # 附加数据，Map类型
        self.optional = None


class BCBatchTransferParams:
    def __init__(self):
        # 渠道类型 目前只支持ALI
        self.channel = BCChannelType.ALI

        # 打款单号
        self.batch_no = None

        # 付款账号账户全称
        self.account_name = None

        # 包含每一笔的具体信息，List类型
        self.transfer_data = None


class BCBatchTransferItem:
    def __init__(self):
        # 打款流水号
        self.transfer_id = None

        # 收款方账户
        self.receiver_account = None

        # 收款方账号姓名
        self.receiver_name = None

        # 打款金额，单位为分
        self.transfer_fee = None

        # 打款备注
        self.transfer_note = None


class BCInternationalPayParams:
    def __init__(self):
        # 渠道类型
        self.channel = None

        # 订单总金额，单位分
        self.total_fee = None

        # 三位货币种类代码
        self.currency = None

        # 商户订单号
        self.bill_no = None

        # 订单标题
        self.title = None

        # 信用卡信息 BCPayPalCreditCard
        self.credit_card_info = None

        # 信用卡id
        self.credit_card_id = None

        # 同步返回页面
        self.return_url = None


class BCPayPalCreditCard:
    def __init__(self):
        # 卡号
        self.card_number = None

        # 过期时间中的月
        self.expire_month = None

        # 过期时间中的年
        self.expire_year = None

        # 信用卡的三位cvv码
        self.cvv = None

        # 用户名字
        self.first_name = None

        # 用户的姓
        self.last_name = None

        # 卡类别
        self.card_type = None


class BCPlan:
    def __init__(self):
        # 订阅计划的唯一标识
        self.id = None

        # 扣款单价
        self.fee = None

        # 扣款周期:day, week, month or year.
        self.interval = None

        # 计划名
        self.name = None

        # ISO货币名，如'CNY'
        self.currency = None

        # 如果是3，那么每3个interval扣款，订阅系统默认1
        self.interval_count = None

        # 试用天数
        self.trial_days = None

        # dict类型的额外信息
        self.optional = None

        # 计划是否生效，查询时返回
        self.valid = None


class BCSubscription:
    def __init__(self):
        # 订阅记录的唯一标识
        self.id = None

        # 订阅的buyer ID，可以是用户email，也可以是商户系统中的用户ID
        self.buyer_id = None

        # 订阅计划id
        self.plan_id = None

        # 由{订阅用户银行名称、订阅用户银行卡号、订阅用户身份证姓名、订阅用户身份证号、订阅用户银行预留手机号}的组合确定
        # 实际发起订阅请求时可以直接使用该id，或者以上的组合
        self.card_id = None

        # 订阅用户银行名称
        self.bank_name = None

        # 订阅用户银行卡号
        self.card_no = None

        # 订阅用户身份证姓名
        self.id_name = None

        # 订阅用户身份证号
        self.id_no = None

        # 订阅用户银行预留手机号
        self.mobile = None

        # 每次扣款总额为 订阅计划的金额 * amount，订阅系统默认为1
        self.amount = None

        # 优惠标识id
        self.coupon_id = None

        # 试用截止时间戳
        self.trial_end = None

        # dict类型的额外信息
        self.optional = None

        # 订阅用户银行卡号后四位，查询时返回
        self.last4 = None

        # 订阅状态，查询时返回
        self.status = None

        # 订阅是否已经生效，查询时返回
        self.valid = None


class BCMerchantUser:
    def __init__(self):
        # 商户的标识，email或者手机号
        self.merchant = None

        # 用户注册时关联的app
        self.app_id = None

        # 用户的ID
        self.buyer_id = None

        # 用户姓名
        self.name = None

        # 用户身份证号
        self.id_no = None

        # 提现卡号
        self.card_no = None

        # 银行卡绑定的手机号
        self.mobile = None

        # 银行全称
        self.bank_name = None

        # 用户类型（等级）。默认为一般用户，默认值0；1 - 认证用户，需通过二要素验证；2 - 可提现用户，需通过四要素认证
        self.buyer_type = None

        # 提现卡类型。0 - 借记卡，1 - 信用卡
        self.card_type = None

        # 该用户注册时间
        self.createdat = None

        # 用户信息修改时间
        self.updatedat = None


class BCCouponTemplate:
    def __init__(self):
        # 卡券模板ID
        self.id = None

        # 卡券模板名称
        self.name = None

        # 卡券类型，0表示满减，1表示折扣
        self.type = None

        # 限制满足额度的条件，以分为单位，0表示不限额，比如满100减10元，返回为10000
        self.limit_fee = None

        # 如果type为0，存储优惠金额，以元为单位，比如10表示减10元；如果type为1，存储折扣比例，例如0.9表示9折
        self.discount = None

        # 卡券总数，0表示不限制
        self.total_count = None

        # 每个人最多可以领取的卡券数量，0表示不限制
        self.max_count_per_user = None

        # 分发的卡券数量
        self.deliver_count = None

        # 使用卡券的数量
        self.use_count = None

        # 卡券有效期类型，1表示根据模板起止时间判断，2表示卡券发放日期后多少天内有效
        self.expiry_type = None

        # 卡券开始时间，可能为null
        self.start_time = None

        # 卡券结束时间，可能为null
        self.end_time = None

        # 卡券发放日期后多少天内有效，在expiry_type为2时有效
        self.delivery_valid_days = None

        # 0表示未开启，1表示正常使用，-1表示停止使用
        self.status = None

        # 卡券所属商家账户
        self.mch_account = None

        # 卡券所属应用
        self.app_id = None

        # 创建时间
        self.created_at = None

        # 更新时间
        self.updated_at = None


class BCCoupon:
    def __init__(self):
        # 卡券ID
        self.id = None

        # 卡券模板
        self.template = None

        # 卡券分发的用户ID，和下单的buyer_id匹配
        self.user_id = None

        # 卡券所属应用
        self.app_id = None

        # 0表示未使用，1表示已使用（核销）
        self.status = None

        # 分发时间
        self.created_at = None

        # 更新时间
        self.updated_at = None

        # 有效期开始时间
        self.start_time = None

        # 有效期结束时间
        self.end_time = None

        # 使用时间，可能为null
        self.use_time = None


class _TmpObject:
    pass
