'''
The fixed point arithmetic parts of this code were originally created by
https://github.com/PetteriAimonen/libfixmath
'''
class VOC_Algorithm():
    '''
    Initialize the VOC algorithm parameters. Call this once at the beginning or
    whenever the sensor stopped measurements.
    '''
    def __init__(self):
        self.VocAlgorithm_SAMPLING_INTERVAL           = (1.)
        self.VocAlgorithm_INITIAL_BLACKOUT            = (45.)
        self.VocAlgorithm_VOC_INDEX_GAIN              = (230.)
        self.VocAlgorithm_SRAW_STD_INITIAL            = (50.)
        self.VocAlgorithm_SRAW_STD_BONUS              = (220.)
        self.VocAlgorithm_TAU_MEAN_VARIANCE_HOURS     = (12.)
        self.VocAlgorithm_TAU_INITIAL_MEAN            = (20.)
        self.VocAlgorithm_INIT_DURATION_MEAN          = ((3600. * 0.75))
        self.VocAlgorithm_INIT_TRANSITION_MEAN        = (0.01)
        self.VocAlgorithm_TAU_INITIAL_VARIANCE        = (2500.)
        self.VocAlgorithm_INIT_DURATION_VARIANCE      = ((3600. * 1.45))
        self.VocAlgorithm_INIT_TRANSITION_VARIANCE    = (0.01)
        self.VocAlgorithm_GATING_THRESHOLD            = (340.)
        self.VocAlgorithm_GATING_THRESHOLD_INITIAL    = (510.)
        self.VocAlgorithm_GATING_THRESHOLD_TRANSITION = (0.09)
        self.VocAlgorithm_GATING_MAX_DURATION_MINUTES = ((60. * 3.))
        self.VocAlgorithm_GATING_MAX_RATIO            = (0.3)
        self.VocAlgorithm_SIGMOID_L                   = (500.)
        self.VocAlgorithm_SIGMOID_K                   = (-0.0065)
        self.VocAlgorithm_SIGMOID_X0                  = (213.)
        self.VocAlgorithm_VOC_INDEX_OFFSET_DEFAULT    = (100.)
        self.VocAlgorithm_LP_TAU_FAST                 = (20.0)
        self.VocAlgorithm_LP_TAU_SLOW                 = (500.0)
        self.VocAlgorithm_LP_ALPHA                    = (-0.2)
        self.VocAlgorithm_PERSISTENCE_UPTIME_GAMMA    = ((3. * 3600.))
        self.VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING = (64.)
        self.VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__FIX16_MAX = (32767.)
        
#       Save the algorithm for VOC
        self.mVoc_Index_Offset = 0
        self.mTau_Mean_Variance_Hours = 0
        self.mGating_Max_Duration_Minutes = 0
        self.mSraw_Std_Initial = 0
        self.mUptime = 0
        self.mSraw = 0
        self.mVoc_Index = 0
        self.m_Mean_Variance_Estimator__Gating_Max_Duration_Minutes = 0
        self.m_Mean_Variance_Estimator___Initialized = True
        self.m_Mean_Variance_Estimator___Mean = 0
        self.m_Mean_Variance_Estimator___Sraw_Offset = 0
        self.m_Mean_Variance_Estimator___Std = 0
        self.m_Mean_Variance_Estimator___Gamma = 0
        self.m_Mean_Variance_Estimator___Gamma_Initial_Mean = 0
        self.m_Mean_Variance_Estimator___Gamma_Initial_Variance = 0
        self.m_Mean_Variance_Estimator__Gamma_Mean = 0
        self.m_Mean_Variance_Estimator__Gamma_Variance = 0
        self.m_Mean_Variance_Estimator___Uptime_Gamma = 0
        self.m_Mean_Variance_Estimator___Uptime_Gating = 0
        self.m_Mean_Variance_Estimator___Gating_Duration_Minutes = 0
        self.m_Mean_Variance_Estimator___Sigmoid__L = 0
        self.m_Mean_Variance_Estimator___Sigmoid__K = 0
        self.m_Mean_Variance_Estimator___Sigmoid__X0 = 0
        self.m_Mox_Model__Sraw_Std = 0
        self.m_Mox_Model__Sraw_Mean = 0
        self.m_Sigmoid_Scaled__Offset = 0
        self.m_Adaptive_Lowpass__A1 = 0
        self.m_Adaptive_Lowpass__A2 = 0
        self.m_Adaptive_Lowpass___Initialized = True
        self.m_Adaptive_Lowpass___X1 = 0
        self.m_Adaptive_Lowpass___X2 = 0
        self.m_Adaptive_Lowpass___X3 = 0
        
#       The maximum value of fix16_t
        self.FIX16_MAXIMUM = 0x7FFFFFFF
        
#       The minimum value of fix16_t
        self.FIX16_MINIMUM = 0x80000000
        
#       fix16_t value of 1
        self.FIX16_ONE = 0x00010000

        self.mVoc_Index_Offset = self.F16(self.VocAlgorithm_VOC_INDEX_OFFSET_DEFAULT)
        self.mTau_Mean_Variance_Hours = self.F16(self.VocAlgorithm_TAU_MEAN_VARIANCE_HOURS)
        self.mGating_Max_Duration_Minutes = self.F16(self.VocAlgorithm_GATING_MAX_DURATION_MINUTES)
        self.mSraw_Std_Initial = self.F16(self.VocAlgorithm_SRAW_STD_INITIAL)
        self.mUptime = self.F16(0.)
        self.mSraw = self.F16(0.)
        self.mVoc_Index = 0
        self.VocAlgorithm__init_instances()
    def uint32_t(self,x):
        return x & 0xffffffff
    
    def fix16_from_int(self,a):
        return int(a * self.FIX16_ONE)
    
    def fix16_cast_to_int(self,a):
        return int(a) >> 16
    
    def F16(self,x):
        if x >= 0:
            return int((x*65536.0 + 0.5))
        else:
            return int((x*65536.0 - 0.5))
     
    def fix16_div(self,a,b):
        '''
        This uses the basic binary restoring division algorithm.
        It appears to be faster to do the whole division manually than
        trying to compose a 64-bit divide out of 32-bit divisions on
        platforms without hardware divide.
        '''
        a = int(a)
        b = int(b)
        if b == 0:
            return self.FIX16_MINIMUM
        if a >= 0:
            remainder =  self.uint32_t(a)
        else:
            remainder = self.uint32_t(-a)
        if b >= 0:
            divider = self.uint32_t(b)
        else:
            divider = self.uint32_t(-b)
        quotient = 0
        bit = 0x10000
#       The algorithm requires D >= R
        while divider < remainder:
            divider <<=  1
            bit <<=  1
            
        if divider & 0x80000000:
            '''
            Perform one step manually to avoid overflows later.
            We know that divider's bottom bit is 0 here.
            '''
            if remainder >= divider: 
                quotient |= bit
                remainder -= divider
            divider >>=  1          
            bit >>=  1
#             Main division loop
        while bit and remainder:
            if remainder >= divider:
                quotient |= bit
                remainder -= divider
            remainder <<=  1
            bit >>= 1
            
        result = quotient
#         Figure out the sign of result
        if ((int(a) ^ int(b)) & 0x80000000):
            result = -result
        return int(result)
    
    def fix16_mul(self,inArg0,inArg1):
        '''
        Each argument is divided to 16-bit parts.
                        AB
                    *   CD
         -----------
                        BD  16 * 16 -> 32 bit products
                        CB
                        AD
                        AC
                    |----| 64 bit product
        '''
        A = (inArg0 >> 16)    
        C = (inArg1 >> 16)
        B = self.uint32_t(inArg0 & 0xFFFF) 
        D = self.uint32_t(inArg1 & 0xFFFF)
        
        AC = (A * C) 
        AD_CB = (A * D) + (C * B)
        BD = B * D

        product_hi = AC + (AD_CB >> 16)
#         Handle carry from lower 32 bits to upper part of result.
        ad_cb_temp = AD_CB << 16

        product_lo = BD + ad_cb_temp
        
        if product_lo < BD:
            product_hi += 1
        '''
        Subtracting 0x8000 (= 0.5) and then using signed right shift
        achieves proper rounding to result-1, except in the corner
        case of negative numbers and lowest word = 0x8000.
        To handle that, we also have to subtract 1 for negative numbers.
        '''
        product_lo_tmp = product_lo
        product_lo -=  0x8000
        product_lo -=  product_hi >> 31

        if product_lo > product_lo_tmp:
            product_hi -= 1
        '''
        Discard the lowest 16 bits. Note that this is not exactly the same
        as dividing by 0x10000. For example if product = -1, result will
        also be -1 and not 0. This is compensated by adding +1 to the result
        and compensating this in turn in the rounding above.
        '''
        result = (product_hi << 16) | (self.uint32_t(product_lo) >> 16)
        result += 1       
        return result
     
    def fix16_exp(self,x):
#       Function to approximate exp(); optimized more for code size than speed
#       exp(x) for x = +/- {1, 1/8, 1/64, 1/512}
        NUM_EXP_VALUES = 4
        exp_pos_values = [self.F16(2.7182818), self.F16(1.1331485), self.F16(1.0157477), self.F16(1.0019550)]
        exp_neg_values = [self.F16(0.3678794), self.F16(0.8824969), self.F16(0.9844964), self.F16(0.9980488)]

        if x > self.F16(10.3972):
            return self.FIX16_MAXIMUM

        if x <= self.F16(-11.7835):
            return 0

        if x < 0:
            x = -x
            exp_values = exp_neg_values
        else:
            exp_values = exp_pos_values
   
        res = self.FIX16_ONE
        arg = self.FIX16_ONE
        for i in range(0,NUM_EXP_VALUES):
            while (x >= arg):
                res = self.fix16_mul(res, exp_values[i])
                x -= arg
            arg >>= 3
            
        return int(res)

    def fix16_sqrt(self,x):
#       It is assumed that x is not negative
        num = self.uint32_t(x)
        result = 0
        n = 0
        bit = self.uint32_t(1 << 30)
        
        while bit > num:
            bit >>= 2
            
        '''
        The main part is executed twice, in order to avoid
        using 64 bit values in computations.
        '''
        for n in range(0,2):
#           First we get the top 24 bits of the answer.
            while bit: 
                if (num >= result + bit): 
                    num -= result + bit
                    result = (result >> 1) + bit
                else: 
                    result = (result >> 1)              
                bit >>= 2
            if n==0:
#               Then process it again to get the lowest 8 bits.
                if num > 65535:
                    '''
                    The remainder 'num' is too large to be shifted left
                    by 16, so we have to add 1 to result manually and
                    adjust 'num' accordingly.
                    num = a - (result + 0.5)^2
                    = num + result^2 - (result + 0.5)^2
                    = num - result - 0.5
                    '''
                    num -= result
                    num = (num << 16) - 0x8000
                    result = (result << 16) + 0x8000
                else: 
                    num <<= 16
                    result <<= 16
                bit = 1 << 14
        return int(result)


    def VocAlgorithm__mean_variance_estimator__set_parameters(self,std_initial,tau_mean_variance_hours,gating_max_duration_minutes):

        self.m_Mean_Variance_Estimator__Gating_Max_Duration_Minutes = gating_max_duration_minutes
        self.m_Mean_Variance_Estimator___Initialized = False
        self.m_Mean_Variance_Estimator___Mean = self.F16(0.)
        self.m_Mean_Variance_Estimator___Sraw_Offset = self.F16(0.)
        self.m_Mean_Variance_Estimator___Std = std_initial
        self.m_Mean_Variance_Estimator___Gamma = self.fix16_div(self.F16((self.VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *
        (self.VocAlgorithm_SAMPLING_INTERVAL / 3600.))),(tau_mean_variance_hours + self.F16(self.VocAlgorithm_SAMPLING_INTERVAL / 3600.)))
        self.m_Mean_Variance_Estimator___Gamma_Initial_Mean = self.F16(((self.VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *
              self.VocAlgorithm_SAMPLING_INTERVAL) / (self.VocAlgorithm_TAU_INITIAL_MEAN + self.VocAlgorithm_SAMPLING_INTERVAL)))
        self.m_Mean_Variance_Estimator___Gamma_Initial_Variance = self.F16(((self.VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *
          self.VocAlgorithm_SAMPLING_INTERVAL) / (self.VocAlgorithm_TAU_INITIAL_VARIANCE + self.VocAlgorithm_SAMPLING_INTERVAL)))
        self.m_Mean_Variance_Estimator__Gamma_Mean = self.F16(0.)
        self.m_Mean_Variance_Estimator__Gamma_Variance = self.F16(0.)
        self.m_Mean_Variance_Estimator___Uptime_Gamma = self.F16(0.)
        self.m_Mean_Variance_Estimator___Uptime_Gating = self.F16(0.)
        self.m_Mean_Variance_Estimator___Gating_Duration_Minutes = self.F16(0.)
    
    def VocAlgorithm__mean_variance_estimator__init(self):
        self.VocAlgorithm__mean_variance_estimator__set_parameters(self.F16(0.),self.F16(0.), self.F16(0.))
        self.VocAlgorithm__mean_variance_estimator___init_instances()
    
    def VocAlgorithm__mean_variance_estimator___init_instances(self):
        self.m_Mean_Variance_Estimator___Sigmoid__L = self.F16(0.)
        self.m_Mean_Variance_Estimator___Sigmoid__K = self.F16(0.)
        self.m_Mean_Variance_Estimator___Sigmoid__X0 = self.F16(0.)      
        
    def VocAlgorithm__mox_model__set_parameters(self,SRAW_STD,SRAW_MEAN):
        self.m_Mox_Model__Sraw_Std = SRAW_STD
        self.m_Mox_Model__Sraw_Mean = SRAW_MEAN
    
    def VocAlgorithm__sigmoid_scaled__set_parameters(self,offset):
        self.m_Sigmoid_Scaled__Offset = offset

    def VocAlgorithm__adaptive_lowpass__set_parameters(self):
        self.m_Adaptive_Lowpass__A1 = self.F16((self.VocAlgorithm_SAMPLING_INTERVAL / (self.VocAlgorithm_LP_TAU_FAST + self.VocAlgorithm_SAMPLING_INTERVAL)))
        self.m_Adaptive_Lowpass__A2  = self.F16((self.VocAlgorithm_SAMPLING_INTERVAL / (self.VocAlgorithm_LP_TAU_SLOW + self.VocAlgorithm_SAMPLING_INTERVAL)))
        self.m_Adaptive_Lowpass___Initialized = False
        
    def VocAlgorithm__init_instances(self):
        self.VocAlgorithm__mean_variance_estimator__init()
        self.VocAlgorithm__mean_variance_estimator__set_parameters(self.mSraw_Std_Initial,self.mTau_Mean_Variance_Hours,self.mGating_Max_Duration_Minutes)
        
        self.m_Mox_Model__Sraw_Std = self.F16(1.)
        self.m_Mox_Model__Sraw_Mean = self.F16(0.)
        self.VocAlgorithm__mox_model__set_parameters(self.m_Mean_Variance_Estimator___Std,(self.m_Mean_Variance_Estimator___Mean + self.m_Mean_Variance_Estimator___Sraw_Offset))
        
        self.m_Sigmoid_Scaled__Offset = self.F16(0.)
        self.VocAlgorithm__sigmoid_scaled__set_parameters(self.mVoc_Index_Offset)
        
        self.VocAlgorithm__adaptive_lowpass__set_parameters()
    
    def VocAlgorithm__mox_model__process(self,sraw):     
        return (self.fix16_mul((self.fix16_div((sraw - self.m_Mox_Model__Sraw_Mean),
                                 (-(self.m_Mox_Model__Sraw_Std +
                                    self.F16(self.VocAlgorithm_SRAW_STD_BONUS))))),
                      self.F16(self.VocAlgorithm_VOC_INDEX_GAIN)))
   
    def VocAlgorithm__sigmoid_scaled__process(self,sample):
        
        x = self.fix16_mul(self.F16(self.VocAlgorithm_SIGMOID_K),
                   (sample - self.F16(self.VocAlgorithm_SIGMOID_X0)));

        if x < self.F16(-50.):
            return self.F16(self.VocAlgorithm_SIGMOID_L)
        
        elif x > self.F16(50.):
            return self.F16(0.)
        
        else:
            if sample >= self.F16(0.):
                shift = self.fix16_div((self.F16(self.VocAlgorithm_SIGMOID_L) - (self.fix16_mul(self.F16(5.), self.m_Sigmoid_Scaled__Offset))),self.F16(4.)) 
                return ((self.fix16_div((self.F16(self.VocAlgorithm_SIGMOID_L) + shift),(self.F16(1.) + self.fix16_exp(x)))) - shift)
            else:
                return (self.fix16_mul((self.fix16_div(self.m_Sigmoid_Scaled__Offset,self.F16(self.VocAlgorithm_VOC_INDEX_OFFSET_DEFAULT))),
                                       (self.fix16_div(self.F16(self.VocAlgorithm_SIGMOID_L),(self.F16(1.) + self.fix16_exp(x))))))
    
    def VocAlgorithm__adaptive_lowpass__process(self,sample):              
        if self.m_Adaptive_Lowpass___Initialized == False:
           self.m_Adaptive_Lowpass___X1 = sample
           self.m_Adaptive_Lowpass___X2 = sample
           self.m_Adaptive_Lowpass___X3 = sample
           self.m_Adaptive_Lowpass___Initialized  = True
        
        self.m_Adaptive_Lowpass___X1 = ((self.fix16_mul((self.F16(1.) - self.m_Adaptive_Lowpass__A1),
                    self.m_Adaptive_Lowpass___X1)) + (self.fix16_mul(self.m_Adaptive_Lowpass__A1, sample)))
        
        self.m_Adaptive_Lowpass___X2 = ((self.fix16_mul((self.F16(1.) - self.m_Adaptive_Lowpass__A2),
                    self.m_Adaptive_Lowpass___X2)) + (self.fix16_mul(self.m_Adaptive_Lowpass__A2, sample)))
        
        abs_delta = (self.m_Adaptive_Lowpass___X1 - self.m_Adaptive_Lowpass___X2)
        
        
        if abs_delta < self.F16(0.):
            abs_delta = -abs_delta
        
        F1 = self.fix16_exp((self.fix16_mul(self.F16(self.VocAlgorithm_LP_ALPHA), abs_delta)))
        
        tau_a = ((self.fix16_mul(self.F16((self.VocAlgorithm_LP_TAU_SLOW - self.VocAlgorithm_LP_TAU_FAST)),F1)) +
         self.F16(self.VocAlgorithm_LP_TAU_FAST))

        a3 = (self.fix16_div(self.F16(self.VocAlgorithm_SAMPLING_INTERVAL),
                    (self.F16(self.VocAlgorithm_SAMPLING_INTERVAL) + tau_a)))

        self.m_Adaptive_Lowpass___X3 = ((self.fix16_mul((self.F16(1.) - a3), self.m_Adaptive_Lowpass___X3)) +
         (self.fix16_mul(a3, sample)))
          
        return self.m_Adaptive_Lowpass___X3

    def VocAlgorithm__mean_variance_estimator___sigmoid__set_parameters(self,L,X0,K):
        self.m_Mean_Variance_Estimator___Sigmoid__L = L
        self.m_Mean_Variance_Estimator___Sigmoid__K = K
        self.m_Mean_Variance_Estimator___Sigmoid__X0 = X0

    def VocAlgorithm__mean_variance_estimator___sigmoid__process(self,sample):
        x = self.fix16_mul(self.m_Mean_Variance_Estimator___Sigmoid__K,
                   (sample - self.m_Mean_Variance_Estimator___Sigmoid__X0))
        
        if x < self.F16(-50.):
            return self.m_Mean_Variance_Estimator___Sigmoid__L
        elif x > self.F16(50.):
            return self.F16(0.)
        else:
            return (self.fix16_div(self.m_Mean_Variance_Estimator___Sigmoid__L,
                            (self.F16(1.) + self.fix16_exp(x))))
        



    def VocAlgorithm__mean_variance_estimator___calculate_gamma(self,voc_index_from_prior):
        uptime_limit = self.F16((self.VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__FIX16_MAX -
                        self.VocAlgorithm_SAMPLING_INTERVAL))
        if self.m_Mean_Variance_Estimator___Uptime_Gamma < uptime_limit:
            self.m_Mean_Variance_Estimator___Uptime_Gamma += self.F16(self.VocAlgorithm_SAMPLING_INTERVAL)
        
        if self.m_Mean_Variance_Estimator___Uptime_Gating < uptime_limit:
            self.m_Mean_Variance_Estimator___Uptime_Gating += self.F16(self.VocAlgorithm_SAMPLING_INTERVAL)

        self.VocAlgorithm__mean_variance_estimator___sigmoid__set_parameters(self.F16(1.), self.F16(self.VocAlgorithm_INIT_DURATION_MEAN),
        self.F16(self.VocAlgorithm_INIT_TRANSITION_MEAN))

        sigmoid_gamma_mean = self.VocAlgorithm__mean_variance_estimator___sigmoid__process(self.m_Mean_Variance_Estimator___Uptime_Gamma)

        gamma_mean = self.m_Mean_Variance_Estimator___Gamma +\
         (self.fix16_mul((self.m_Mean_Variance_Estimator___Gamma_Initial_Mean -
                    self.m_Mean_Variance_Estimator___Gamma),sigmoid_gamma_mean))

        gating_threshold_mean =\
        (self.F16(self.VocAlgorithm_GATING_THRESHOLD) +
         (self.fix16_mul(
            self.F16((self.VocAlgorithm_GATING_THRESHOLD_INITIAL -
                self.VocAlgorithm_GATING_THRESHOLD)),
            self.VocAlgorithm__mean_variance_estimator___sigmoid__process(self.m_Mean_Variance_Estimator___Uptime_Gating))))

        self.VocAlgorithm__mean_variance_estimator___sigmoid__set_parameters(self.F16(1.), gating_threshold_mean,
        self.F16(self.VocAlgorithm_GATING_THRESHOLD_TRANSITION))

        sigmoid_gating_mean = self.VocAlgorithm__mean_variance_estimator___sigmoid__process(voc_index_from_prior)
        self.m_Mean_Variance_Estimator__Gamma_Mean = self.fix16_mul(sigmoid_gating_mean, gamma_mean)
        self.VocAlgorithm__mean_variance_estimator___sigmoid__set_parameters(self.F16(1.),self.F16(self.VocAlgorithm_INIT_DURATION_VARIANCE),
        self.F16(self.VocAlgorithm_INIT_TRANSITION_VARIANCE))
        sigmoid_gamma_variance = self.VocAlgorithm__mean_variance_estimator___sigmoid__process(
            self.m_Mean_Variance_Estimator___Uptime_Gamma)
        
        gamma_variance =\
        (self.m_Mean_Variance_Estimator___Gamma +
         (self.fix16_mul(
             (self.m_Mean_Variance_Estimator___Gamma_Initial_Variance -
              self.m_Mean_Variance_Estimator___Gamma),
             (sigmoid_gamma_variance - sigmoid_gamma_mean))))

        gating_threshold_variance =\
        (self.F16(self.VocAlgorithm_GATING_THRESHOLD) +
         (self.fix16_mul(
             self.F16((self.VocAlgorithm_GATING_THRESHOLD_INITIAL -
                  self.VocAlgorithm_GATING_THRESHOLD)),
             self.VocAlgorithm__mean_variance_estimator___sigmoid__process(self.m_Mean_Variance_Estimator___Uptime_Gating))))
        
        self.VocAlgorithm__mean_variance_estimator___sigmoid__set_parameters(self.F16(1.), gating_threshold_variance,
        self.F16(self.VocAlgorithm_GATING_THRESHOLD_TRANSITION))

        sigmoid_gating_variance =\
        self.VocAlgorithm__mean_variance_estimator___sigmoid__process(voc_index_from_prior)
        self.m_Mean_Variance_Estimator__Gamma_Variance =\
        self.fix16_mul(sigmoid_gating_variance, gamma_variance)
        self.m_Mean_Variance_Estimator___Gating_Duration_Minutes =\
        self.m_Mean_Variance_Estimator___Gating_Duration_Minutes +\
         (self.fix16_mul(self.F16((self.VocAlgorithm_SAMPLING_INTERVAL / 60.)),
                    ((self.fix16_mul((self.F16(1.) - sigmoid_gating_mean),
                                self.F16((1. + self.VocAlgorithm_GATING_MAX_RATIO)))) -
                     self.F16(self.VocAlgorithm_GATING_MAX_RATIO))))

        if self.m_Mean_Variance_Estimator___Gating_Duration_Minutes < self.F16(0.):
            self.m_Mean_Variance_Estimator___Gating_Duration_Minutes = self.F16(0.)
        
        if self.m_Mean_Variance_Estimator___Gating_Duration_Minutes >\
            self.m_Mean_Variance_Estimator__Gating_Max_Duration_Minutes:
            self.m_Mean_Variance_Estimator___Uptime_Gating = self.F16(0.)
        

    def VocAlgorithm__mean_variance_estimator__process(self,sraw,voc_index_from_prior): 
        
        if self.m_Mean_Variance_Estimator___Initialized == False:
            self.m_Mean_Variance_Estimator___Initialized = True
            self.m_Mean_Variance_Estimator___Sraw_Offset = sraw
            self.m_Mean_Variance_Estimator___Mean = self.F16(0.)
        else:
            if self.m_Mean_Variance_Estimator___Mean >= self.F16(100.) or self.m_Mean_Variance_Estimator___Mean <= self.F16(100.):
                self.m_Mean_Variance_Estimator___Sraw_Offset =(self.m_Mean_Variance_Estimator___Sraw_Offset +
                self.m_Mean_Variance_Estimator___Mean)
                self.m_Mean_Variance_Estimator___Mean = self.F16(0.)

            sraw = sraw - self.m_Mean_Variance_Estimator___Sraw_Offset
            self.VocAlgorithm__mean_variance_estimator___calculate_gamma(voc_index_from_prior)
        
            delta_sgp = (self.fix16_div(
                (sraw - self.m_Mean_Variance_Estimator___Mean),
                self.F16(self.VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING)))
            if delta_sgp < self.F16(0.):
                c = self.m_Mean_Variance_Estimator___Std - delta_sgp
            else:
                c = self.m_Mean_Variance_Estimator___Std + delta_sgp
            additional_scaling = self.F16(1.)
            if c > self.F16(1440.):
                additional_scaling = self.F16(4.)

            self.m_Mean_Variance_Estimator___Std = (self.fix16_mul(
                self.fix16_sqrt((self.fix16_mul(
                    additional_scaling,
                    (self.F16(self.VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING) -
                    self.m_Mean_Variance_Estimator__Gamma_Variance)))),
                self.fix16_sqrt((
                    (self.fix16_mul(
                        self.m_Mean_Variance_Estimator___Std,
                        (self.fix16_div(
                           self.m_Mean_Variance_Estimator___Std,
                            (self.fix16_mul(
                                self.F16(self.VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING),
                                additional_scaling)))))) +
                    (self.fix16_mul(
                        (self.fix16_div(
                            (self.fix16_mul(
                                self.m_Mean_Variance_Estimator__Gamma_Variance,
                                delta_sgp)),
                            additional_scaling)),
                        delta_sgp))))))

            self.m_Mean_Variance_Estimator___Mean =\
                    (self.m_Mean_Variance_Estimator___Mean +
                    (self.fix16_mul(self.m_Mean_Variance_Estimator__Gamma_Mean,
                            delta_sgp)))
    '''
    Calculate the VOC index value from the raw sensor value.
    sraw : Raw value from the SGP40 sensor
    
    Calculated VOC index value from the raw sensor value. Zero
    during initial blackout period and 1..500 afterwards
    '''
    def VocAlgorithm_process(self,sraw):
        if (self.mUptime <= self.F16(self.VocAlgorithm_INITIAL_BLACKOUT)):
              self.mUptime += self.F16(self.VocAlgorithm_SAMPLING_INTERVAL)
              return 0
        else:           
            if (((sraw > 0) and (sraw < 65000))):
                if ((sraw < 20001)):
                    sraw = 20001
                elif ((sraw > 52767)):
                    sraw = 52767           
                self.mSraw = (self.fix16_from_int((sraw - 20000)))
            self.mVoc_Index = self.VocAlgorithm__mox_model__process(self.mSraw)
            self.mVoc_Index = self.VocAlgorithm__sigmoid_scaled__process(self.mVoc_Index)
            self.mVoc_Index = self.VocAlgorithm__adaptive_lowpass__process(self.mVoc_Index)
           
            if self.mVoc_Index < self.F16(0.5):
                self.mVoc_Index = self.F16(0.5)
            
            if self.mSraw > self.F16(0.):
                self.VocAlgorithm__mean_variance_estimator__process(self.mSraw,self.mVoc_Index)
                self.VocAlgorithm__mox_model__set_parameters(self.m_Mean_Variance_Estimator___Std,
                (self.m_Mean_Variance_Estimator___Mean + self.m_Mean_Variance_Estimator___Sraw_Offset))

            return self.fix16_cast_to_int(self.mVoc_Index + self.F16(0.5))
        



