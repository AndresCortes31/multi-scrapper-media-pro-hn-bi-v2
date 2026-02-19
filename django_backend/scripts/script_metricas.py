import os
import sys
import django
import datetime
import json
from django.db.models import Count, Avg
from django.db.models.functions import ExtractWeekDay
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, FloatField

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django_backend.models import ScrapeResult

def mostrar_metricas():
    print("="*40)
    print("   DASHBOARD DE MÉTRICAS REALES")
    print("="*40)

    hace_una_semana = timezone.now() - datetime.timedelta(days=7)
    dias_map = {1: 'Sun', 2: 'Mon', 3: 'Tue', 4: 'Wed', 5: 'Thu', 6: 'Fri', 7: 'Sat'}

    total_posts = ScrapeResult.objects.count()
    if total_posts == 0:
        print("La base de datos está vacía.")
        return

    total_profiles = ScrapeResult.objects.values('username').distinct().count()
    
    avg_engagement_pct = ScrapeResult.objects.filter(followers__gt=0).annotate(
        engagement_post=ExpressionWrapper(
            (F('likes') + F('comments')) * 100.0 / F('followers'),
            output_field=FloatField()
        )
    ).aggregate(Avg('engagement_post'))['engagement_post__avg'] or 0

    avg_engagement = f"{round(avg_engagement_pct, 2)}%"

    volumen_semanal_raw = (
        ScrapeResult.objects.filter(created_at__gte=hace_una_semana)
        .annotate(day_num=ExtractWeekDay('created_at'))
        .values('day_num')
        .annotate(count=Count('id'))
    )
    
    weekly_stats = {dias_map[item['day_num']]: item['count'] for item in volumen_semanal_raw}

    dist = ScrapeResult.objects.values('platform').annotate(total=Count('id'))
    platform_dist = {}
    for item in dist:
        p_name = item['platform'].capitalize()
        percentage = (item['total'] / total_posts) * 100
        platform_dist[p_name] = f"{round(percentage, 1)}%"

    metricas = {
        "Posts Extracted": total_posts,
        "Total Profiles": total_profiles,
        "Avg Engagement": avg_engagement,
        "Platform Distribution": platform_dist,
        "Extraction Volume (Weekly)": weekly_stats
    }

    print(json.dumps(metricas, indent=4))

if __name__ == "__main__":
    mostrar_metricas()