from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
# _('') 를 사용해 표현한 string 들은 translation이 되어지도록 만들어준다.
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = '유저'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['date_joined']

    def __str__(self):
        return f'{self.name}'

    CHRONIC_RENAL_DISEASE_CHOICES = (
        ('1단계', 'GFR > 90'),
        ('2단계', 'GFR 60~90'),
        ('3단계', 'GFR 30~60'),
        ('4단계', 'GFR 15~30'),
        ('5단계', 'GFR < 15(신부전, 투석)'),
    )

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        help_text=_('Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(_('Name'), max_length=20)
    gender = models.BooleanField(_('Gender'), default=True)
    height = models.PositiveSmallIntegerField(_('Height'), blank=True, null=True)
    weight = models.PositiveSmallIntegerField(_('Weight'), blank=True, null=True)
    renal_disease = models.CharField(
        max_length=3,
        choices=CHRONIC_RENAL_DISEASE_CHOICES,
        default='1단계',
        blank=True,
        null=True
    )
    email = models.EmailField(_('Email Address'), blank=True, null=True)
    phone_number = models.CharField(_('Phone Number'), max_length=12, blank=True, null=True)
    hospital = models.CharField(_('Hospital'), max_length=30, blank=True, null=True)
    attending_physician = models.CharField(_('Attending Physician'), max_length=30, blank=True, null=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # 각 모델은 기본적으로 데이터베이스 쿼리와 연동되는 모델 매니저를 갖는다.
    # 디폴트 모델 매니저는 objects이다.
    # ex) User.objects.filter()
    # 아래와 같이 objects에 커스텀 모델 매니저를 추가하거나, 다른 이름의 모델 매니저를 추가할 수도 있다.
    # refernce : https://wikidocs.net/6668
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)