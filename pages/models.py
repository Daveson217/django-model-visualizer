from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from django.utils import timezone
from datetime import datetime, timedelta, time
# 3rd party
from django.conf import settings
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, default='david@email.com')
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    #def get_absolute_url(self):
    #    return reverse("Article_detail", kwargs={"pk": self.pk})

class Saver(models.Model):
    saver_code = models.CharField(_("Saver Code"), max_length=50, unique=True, blank=True, null=True)
    first_name = models.CharField(_("First Name"), max_length=90, blank=False, default="")        
    middle_name = models.CharField(_("Middle Name"), max_length=90, blank=True, default="")   
    last_name = models.CharField(_("Last Name"), max_length=90, blank=False, default="")          
    address = models.CharField(_("Address"), max_length=255, blank=False, default="")         
    lga = models.CharField(_("LGA"), max_length=70, blank=False)
    state = models.CharField(_("State"),
        choices= [             
            ("Sokoto", "Sokoto"),
            ("Taraba", "Taraba"),
            ("Yobe", "Yobe"),
            ("Zamfara", "Zamfara"),    
        ], max_length=70, blank=False)
    saving_frequency = models.CharField(_("Saving Frequency"), 
        max_length=15,
        choices= [        
            ('DAILY', 'DAILY'),
            ('WEEKLY', 'WEEKLY'),
            ('MONTHLY', 'MONTHLY'),
        ],
        default='DAILY')
    saving_amount = models.IntegerField(_("Saving Amount"))
    saving_target = models.IntegerField(_("Saving Target"))
    account_number = models.CharField(_("Account Number"), max_length=15, blank=True)
    account_name = models.CharField(_("Account Name"), max_length=50, blank=True)
    bank = models.CharField(_("Bank"),
        choices = [            
            ('Zenith Bank', 'Zenith Bank'),            
        ], max_length=50, blank=True)    
    date_joined = models.DateTimeField(auto_now_add=True)
    #picture = models.ImageField(null=True, blank=False, height_field=None, width_field=None, max_length=254)          
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    # add picture        
    class Meta:
        verbose_name = _("Saver")
        verbose_name_plural = _("Savers")

    def __str__(self):
        return f'{self.first_name} {self.last_name}' 
class DepositManager(models.Manager):
    
    today = timezone.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    
    def get_deposits_today(self):
        """Returns the sum of deposits each day

        Returns:
            int: Sum of deposits
        """        
        return sum( deposit.amount for deposit in self.filter(date_time__lte=self.today_end, date_time__gte=self.today_start))
class Deposit(models.Model):
    saver = models.ForeignKey(Saver, verbose_name=_("Saver"), on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)   
    amount = models.PositiveIntegerField(_("Amount in Naira"), blank=False, default=0)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    
    objects = DepositManager()

    def __str__(self):
        return str(self.amount)

    class Meta:   
        verbose_name = _('Deposit')
        verbose_name_plural = _('Deposits')

class WithdrawalManager(models.Manager):
    
    today = timezone.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    
    def get_withdrawals_today(self):
        """Returns the sum of withdrawals each day

        Returns:
            int: Sum of withdrawals
        """        
        return sum( deposit.amount for deposit in self.filter(date_time__lte=self.today_end, date_time__gte=self.today_start))

class Withdrawal(models.Model):
    saver = models.ForeignKey(Saver, verbose_name=_("Saver"), on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)   
    amount = models.PositiveIntegerField(_("Amount in Naira"), blank=False, default=0)
    is_validated = models.BooleanField(default=False)    
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL) 
    
    objects = WithdrawalManager()
    
    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = _('Withdrawal')
        verbose_name_plural = _('Withdrawals')
        
        
class OTP(models.Model):
    otp_code = models.CharField(_("OTP Code"), max_length=10,)
    withdrawal = models.ForeignKey("Withdrawal", on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)            
    expire_at = models.DateTimeField(_("Expiry date"))

    class Meta:
        verbose_name = _("OTP")
        verbose_name_plural = _("OTPs")

    def __str__(self):
        return self.otp_code