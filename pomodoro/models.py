from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

VALIDATORS_GENERIC_MINUTES: list = [
    MinValueValidator(1), MaxValueValidator(99)]
VALIDATOR_MIN_ITERATIONS = MinValueValidator(2)
VALIDATOR_MAX_ITERATIONS = MaxValueValidator(10)


DEFAULT_POMODORO = 25
DEFAULT_SMALL_REST = 5
DEFAULT_LONG_REST = 15
DEFAULT_ITERATIONS = 4


class PomodoroSettingToUser(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    pomodoro = models.IntegerField(default=DEFAULT_POMODORO,
                                   validators=VALIDATORS_GENERIC_MINUTES)
    small_rest = models.IntegerField(default=DEFAULT_SMALL_REST,
                                     validators=VALIDATORS_GENERIC_MINUTES)
    iterations_before_long_break = models.IntegerField(default=DEFAULT_ITERATIONS,
                                                       validators=[VALIDATOR_MIN_ITERATIONS, VALIDATOR_MAX_ITERATIONS])
    long_break = models.IntegerField(default=DEFAULT_LONG_REST,
                                     validators=VALIDATORS_GENERIC_MINUTES)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        true_record = self._get_active_record_for_current_user_or_none()
        self._check_true_record_and_switch_active_if_current_is_active(true_record)
        return super().save(*args, **kwargs)
    
    def _check_true_record_and_switch_active_if_current_is_active(self, true_record: any):
        if true_record and true_record != self and true_record.active and self.active:
            true_record.active = False
            true_record.save()
    
    def _get_active_record_for_current_user_or_none(self):
        try:
            true_record = PomodoroSettingToUser.objects.get(active=True, user=self.user)
        except ObjectDoesNotExist:
            true_record = None
        return true_record