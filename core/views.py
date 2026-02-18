from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .forms import ContactForm

# Імпортуємо моделі з інших додатків
from posts.models import Post, Hashtag
from forum.models import Topic
from gallery.models import MediaItem
from portfolio.models import PortfolioItem
from events.models import Event
from announcements.models import Announcement
from surveys.models import Survey
from votes.models import Vote

User = get_user_model()

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Останні пости
        context['latest_posts'] = Post.objects.all().order_by('-created_at')[:5]
        
        # Популярні хештеги
        context['trending_hashtags'] = Hashtag.objects.annotate(
            post_count=Count('posts')
        ).order_by('-post_count')[:10]
        
        # Активні події
        now = timezone.now()
        context['upcoming_events'] = Event.objects.filter(
            date__gte=now, 
            is_active=True
        ).order_by('date')[:3]
        
        # Останні оголошення
        context['latest_announcements'] = Announcement.objects.filter(
            is_pinned=True
        ).order_by('-created_at')[:3]
        
        # Активні голосування
        context['active_votes'] = Vote.objects.filter(
            is_active=True
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gt=now)
        )[:3]
        
        # Статистика
        context['stats'] = {
            'users_count': User.objects.count(),
            'posts_count': Post.objects.count(),
            'topics_count': Topic.objects.count(),
            'gallery_count': MediaItem.objects.filter(is_approved=True).count(),
            'portfolio_count': PortfolioItem.objects.filter(is_approved=True).count(),
        }
        
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['developers'] = [
            {'name': 'Команда CS2 MicroTwitter', 'role': 'Розробники'}
        ]
        context['version'] = '1.0.0'
        return context

class RulesView(TemplateView):
    template_name = 'core/rules.html'

class ContactView(FormView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact_success')
    
    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'core/contact_success.html'

class HelpView(TemplateView):
    template_name = 'core/help.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_topics'] = [
            {
                'title': 'Як створити пост?',
                'content': 'Для створення поста перейдіть на головну сторінку та натисніть кнопку "Написати пост".'
            },
            {
                'title': 'Як завантажити медіа в галерею?',
                'content': 'Перейдіть до галереї та натисніть кнопку "Завантажити". Виберіть тип медіа та файл.'
            },
            {
                'title': 'Як додати хайлайт до портфоліо?',
                'content': 'У своєму профілі перейдіть до розділу "Портфоліо" та натисніть "Додати хайлайт".'
            },
            {
                'title': 'Як взяти участь у голосуванні?',
                'content': 'Перейдіть до розділу "Голосування", оберіть активне голосування та проголосуйте.'
            },
        ]
        return context

class FAQView(TemplateView):
    template_name = 'core/faq.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faq_items'] = [
            {
                'question': 'Що таке CS2 MicroTwitter?',
                'answer': 'Це соціальна мережа для фанатів Counter-Strike 2, де можна ділитися хайлайтами, обговорювати матчі та патчі.'
            },
            {
                'question': 'Чи потрібна реєстрація?',
                'answer': 'Так, для створення постів, коментарів та завантаження медіа потрібна реєстрація.'
            },
            {
                'question': 'Як стати модератором?',
                'answer': 'Модератори призначаються адміністрацією сайту за активну участь у житті спільноти.'
            },
            {
                'question': 'Чи можна завантажувати демо-файли?',
                'answer': 'Так, ви можете завантажувати демо-файли в розділі "Портфоліо".'
            },
            {
                'question': 'Як повідомити про порушення?',
                'answer': 'Ви можете зв\'язатися з модераторами через форму контактів або написати в Telegram.'
            },
        ]
        return context

class StatsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/stats.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # Загальна статистика
        context['total_users'] = User.objects.count()
        context['total_posts'] = Post.objects.count()
        context['total_comments'] = Post.objects.aggregate(total=Count('comments'))['total']
        context['total_topics'] = Topic.objects.count()
        context['total_messages'] = Topic.objects.aggregate(total=Count('messages'))['total']
        context['total_gallery'] = MediaItem.objects.filter(is_approved=True).count()
        context['total_portfolio'] = PortfolioItem.objects.filter(is_approved=True).count()
        context['total_surveys'] = Survey.objects.count()
        context['total_votes'] = Vote.objects.count()
        
        # Статистика за останній тиждень
        context['new_users_week'] = User.objects.filter(date_joined__gte=week_ago).count()
        context['new_posts_week'] = Post.objects.filter(created_at__gte=week_ago).count()
        context['new_topics_week'] = Topic.objects.filter(created_at__gte=week_ago).count()
        
        # Статистика за останній місяць
        context['new_users_month'] = User.objects.filter(date_joined__gte=month_ago).count()
        context['new_posts_month'] = Post.objects.filter(created_at__gte=month_ago).count()
        context['new_topics_month'] = Topic.objects.filter(created_at__gte=month_ago).count()
        
        # Топ-користувачі
        context['top_users'] = User.objects.annotate(
            post_count=Count('posts')
        ).order_by('-post_count')[:5]
        
        context['top_posters'] = User.objects.annotate(
            post_count=Count('posts')
        ).order_by('-post_count')[:5]
        
        context['top_commenters'] = User.objects.annotate(
            comment_count=Count('comments')
        ).order_by('-comment_count')[:5]
        
        # Активність за останні 7 днів
        activity = []
        for i in range(7):
            day = now - timedelta(days=i)
            activity.append({
                'date': day.strftime('%d.%m'),
                'posts': Post.objects.filter(created_at__date=day.date()).count(),
                'topics': Topic.objects.filter(created_at__date=day.date()).count(),
                'users': User.objects.filter(date_joined__date=day.date()).count(),
            })
        context['activity'] = activity[::-1]
        
        return context

class GlobalSearchView(ListView):
    template_name = 'core/search.html'
    context_object_name = 'results'
    paginate_by = 20
    
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return []
        
        results = []
        
        # Пошук у постах
        posts = Post.objects.filter(
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )[:10]
        results.extend([('post', post) for post in posts])
        
        # Пошук у темах форуму
        topics = Topic.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(created_by__username__icontains=query)
        )[:10]
        results.extend([('topic', topic) for topic in topics])
        
        # Пошук у галереї
        gallery_items = MediaItem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(user__username__icontains=query),
            is_approved=True
        )[:10]
        results.extend([('gallery', item) for item in gallery_items])
        
        # Пошук у портфоліо
        portfolio_items = PortfolioItem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(user__username__icontains=query),
            is_approved=True
        )[:10]
        results.extend([('portfolio', item) for item in portfolio_items])
        
        # Пошук користувачів
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )[:10]
        results.extend([('user', user) for user in users])
        
        return results
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class StatusView(TemplateView):
    template_name = 'core/status.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        import time
        start_time = time.time()
        
        # Перевіряємо підключення до бази даних
        try:
            User.objects.first()
            db_status = 'ok'
        except Exception:
            db_status = 'error'
        
        response_time = int((time.time() - start_time) * 1000)
        
        context['status'] = {
            'database': db_status,
            'response_time': response_time,
            'server_time': timezone.now().strftime('%d.%m.%Y %H:%M:%S'),
            'users_online': User.objects.filter(last_login__gte=timezone.now() - timedelta(minutes=15)).count(),
            'total_users': User.objects.count(),
            'total_posts': Post.objects.count(),
        }
        
        return context

class SitemapView(TemplateView):
    template_name = 'core/sitemap.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['sections'] = [
            {
                'name': 'Головна',
                'url': '/',
                'items': []
            },
            {
                'name': 'Пости',
                'url': '/posts/',
                'items': Post.objects.all()[:10]
            },
            {
                'name': 'Форум',
                'url': '/forum/',
                'items': Topic.objects.all()[:10]
            },
            {
                'name': 'Галерея',
                'url': '/gallery/',
                'items': MediaItem.objects.filter(is_approved=True)[:10]
            },
            {
                'name': 'Портфоліо',
                'url': '/portfolio/',
                'items': PortfolioItem.objects.filter(is_approved=True)[:10]
            },
            {
                'name': 'Події',
                'url': '/events/',
                'items': Event.objects.filter(is_active=True)[:10]
            },
            {
                'name': 'Голосування',
                'url': '/votes/',
                'items': Vote.objects.filter(is_active=True)[:10]
            },
        ]
        
        return context

class APIInfoView(TemplateView):
    template_name = 'core/api_info.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['endpoints'] = [
            {
                'name': 'Пости',
                'url': '/api/posts/',
                'methods': ['GET', 'POST'],
                'description': 'Отримання списку постів та створення нових'
            },
            {
                'name': 'Коментарі',
                'url': '/api/comments/',
                'methods': ['GET', 'POST'],
                'description': 'Робота з коментарями'
            },
            {
                'name': 'Користувачі',
                'url': '/api/users/',
                'methods': ['GET'],
                'description': 'Інформація про користувачів'
            },
            {
                'name': 'Галерея',
                'url': '/api/gallery/',
                'methods': ['GET'],
                'description': 'Отримання медіа з галереї'
            },
        ]
        
        return context

class SupportView(TemplateView):
    template_name = 'core/support.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['support_options'] = [
            {
                'title': 'Telegram',
                'description': 'Приєднуйтесь до нашого Telegram каналу',
                'link': 'https://t.me/cs2microtwitter',
                'icon': 'telegram'
            },
            {
                'title': 'Discord',
                'description': 'Спілкуйтесь з іншими фанатами CS2',
                'link': 'https://discord.gg/cs2microtwitter',
                'icon': 'discord'
            },
            {
                'title': 'GitHub',
                'description': 'Вихідний код проекту',
                'link': 'https://github.com/cs2microtwitter',
                'icon': 'github'
            },
        ]
        
        context['donate_options'] = [
            {
                'title': 'Підтримати проект',
                'description': 'Допоможіть розвитку спільноти',
                'methods': ['PayPal', 'Patreon', 'Buy Me a Coffee']
            }
        ]
        
        return context

class Custom404View(TemplateView):
    template_name = 'core/404.html'

class Custom500View(TemplateView):
    template_name = 'core/500.html'