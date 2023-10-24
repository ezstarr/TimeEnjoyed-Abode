# Generated by Django 4.1 on 2023-10-06 07:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0016_alter_readrequest_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="Zodiac_Sun_Sign",
        ),
        migrations.AddField(
            model_name="profile",
            name="user_zodiac",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ARI", "Aries (March 21 - April 19)"),
                    ("TAU", "Taurus (April 20 – May 20)"),
                    ("GEM", "Gemini (May 21 – June 20)"),
                    ("CAN", "Cancer (June 21 – July 22)"),
                    ("LEO", "Leo (July 23 – August 22)"),
                    ("VIR", "Virgo (August 23 – September 22)"),
                    ("LIB", "Libra (September 23 – October 22)"),
                    ("SCO", "Scorpio (October 23 – November 21)"),
                    ("SAG", "Sagittarius (November 22 – December 21)"),
                    ("CAP", "Capricorn (December 22 – January 19)"),
                    ("AQU", "Aquarius (January 20 – February 18)"),
                    ("PIS", "Pisces (February 19 – March 20)"),
                ],
                default=None,
                max_length=3,
                null=True,
            ),
        ),
    ]