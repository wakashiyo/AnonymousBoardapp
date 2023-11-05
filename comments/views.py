from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CommentForm
from .models import Comment, Like
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods as require_http
from django.contrib.auth.decorators import login_required
from django.db import transaction




# ページネーション機能
def paginate_queryset(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # ページ数が整数でない場合、最初のページを返す
        page_obj = paginator.page(1)
    except EmptyPage:
        # ページが存在しない場合、最後のページを返す
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


# コメント一覧表示機能
def comments_index(request):
    paginate = request.GET.get(key="paginate", default="6")
    comments_list = Comment.objects.filter(parent_comment__isnull=True).order_by('-created_at')  # 返信を除外して親コメントのみ取得
    page_obj = paginate_queryset(request, comments_list, paginate)
    context = {
        'comments': page_obj.object_list,
        'page_obj': page_obj,
        'paginate': paginate,
    }
    return render(request, 'comments/index.html', context)


# コメント投稿機能
def comments_create(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.body = form.cleaned_data.get('body')
            comment.file = form.cleaned_data.get('file')
            comment.password = form.cleaned_data.get('password')
            comment.save()
            messages.success(request, 'コメントを投稿しました。', extra_tags='success_message')
            return redirect(reverse('comments:index'))
        else:
            # エラーメッセージをつけて返す
            context = {}
            context['page_title'] = 'コメントの投稿'
            context['form_name'] = 'コメントの投稿'
            context['button_label'] = 'コメントを投稿する'
            context['form'] = form
            return render(request, 'comments/form.html', context)
    else:
        context = {}
        context['form'] = CommentForm(
            initial={
            }
        )
        context['page_title'] = 'コメントの投稿'
        context['form_name'] = 'コメントの投稿'
        context['button_label'] = 'コメントを投稿する'
        return render(request, 'comments/form.html', context)


# パスワード認証機能
def password_auth(view_func):
    def wrapped_view(request, *args, **kwargs):
        # パスワード認証処理
        comment_id = kwargs.get('comment_id')
        password = request.POST.get('password')

        #  コメントを取得
        comment = get_object_or_404(Comment, pk=comment_id)

        # パスワードの確認
        if password == comment.password:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'パスワードが違います。', extra_tags='error_message')
            return redirect(reverse('comments:index'))
    return wrapped_view


# コメント編集機能
def comments_update(request, comment_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid(): 
            comment = get_object_or_404(Comment, pk=comment_id)
            password = form.cleaned_data.get('password')

            # パスワード認証
            if password == comment.password:
                comment.body = form.cleaned_data.get('body')
                comment.save()
                messages.success(request, 'コメントを更新しました。', extra_tags='success_message')
                return redirect(reverse('comments:index'))
            else:
                messages.error(request, 'パスワードが違います。', extra_tags='error_message')
                return redirect(reverse('comments:index'))
        else:
            context = {}
            context['page_title'] = 'コメントの編集'
            context['form_name'] = 'コメントの編集'
            context['button_label'] = 'コメントを更新する'
            context['form'] = form
            return render(request, 'comments/form.html', context)
    else:
        context = {}
        comment = get_object_or_404(Comment, pk=comment_id)
        context['form'] = CommentForm(
            initial={
                'body' : comment.body,
            }
        )
        context['comment'] = comment
        context['page_title'] = 'コメントの編集'
        context['form_name'] = 'コメントの編集'
        context['button_label'] = 'コメントを更新する'
        return render(request, 'comments/form.html', context)


# コメント削除機能
def comments_delete(request, comment_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid(): 
            comment = get_object_or_404(Comment, pk=comment_id)
            password = form.cleaned_data.get('password')

            # パスワード認証
            if password == comment.password:
                comment.body = form.cleaned_data.get('body')
            
                # 返信コメントを削除
                child_comments = Comment.objects.filter(parent_comment=comment)
                for child_comment in child_comments:
                    child_comment.delete()
                comment.delete()
                messages.success(request, 'コメントを削除しました。', extra_tags='success_message')
                return redirect(reverse('comments:index'))
            else:
                messages.error(request, 'パスワードが違います。', extra_tags='error_message')
                return redirect(reverse('comments:index'))
        else:
            context = {}
            context['page_title'] = 'コメントの削除'
            context['form_name'] = 'コメントを削除しますか？'
            context['button_label'] = 'コメントを削除する'
            context['form'] = form
            return render(request, 'comments/form.html', context)
    else:
        context = {}
        comment = get_object_or_404(Comment, pk=comment_id)
        context['form'] = CommentForm(
            initial={
                'body' : comment.body,
            }
        )
        context['comment'] = comment
        context['page_title'] = 'コメントの削除'
        context['form_name'] = 'コメントを削除しますか？'
        context['button_label'] = 'コメントを削除する'
        return render(request, 'comments/form.html', context)


# 返信追加機能
def comments_reply(request, comment_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_comment = get_object_or_404(Comment, pk=comment_id)
            comment = form.save(commit=False)
            comment.parent_comment = parent_comment
            comment.save()
            messages.success(request, '返信を投稿しました。', extra_tags='success_message')
            return redirect(reverse('comments:index'))
        else:
            # エラーメッセージをつけて返す
            context = {}
            context['page_title'] = 'コメントの返信'
            context['form_name'] = 'コメントの返信'
            context['button_label'] = 'コメントに返信する'
            context['form'] = form
            return render(request, 'comments/form.html', context)
    else:
        context = {}
        context['form'] = CommentForm(
            initial={
            }
        )
        context['page_title'] = 'コメントの返信'
        context['form_name'] = 'コメントの返信'
        context['button_label'] = 'コメントに返信する'
        return render(request, 'comments/form.html', context)


# コメント詳細表示機能
def comments_show(request, comment_id):
    context = {}
    comment = get_object_or_404(Comment, pk=comment_id)
    context['comment'] = comment


    # 返信がついていない場合
    if comment.parent_comment is None:
        # 直前（自身の直後に更新されたコメント）を取得する
        prev_comment = Comment.objects.filter(updated_at__gt=comment.updated_at).exclude(parent_comment__isnull=False).order_by('updated_at').first()

        # 直後（自身の直前に更新されたコメント）を取得する
        next_comment = Comment.objects.filter(updated_at__lt=comment.updated_at).exclude(parent_comment__isnull=False).order_by('-updated_at').first()

        if prev_comment is not None:
            prev_id = prev_comment.id
        else:
            prev_id = False
        if next_comment is not None:
            next_id = next_comment.id
        else:
            next_id = False
        context['prev_id'] = prev_id
        context['next_id'] = next_id
    else:
        # 次のparent_commentがないコメントを取得する
        next_parent_comment = Comment.objects.filter(parent_comment=comment.parent_comment, updated_at__gt=comment.updated_at).exclude(parent_comment__isnull=False).order_by('updated_at').first()

        # 次のparent_commentが存在する場合はそのコメントを取得する
        if next_parent_comment is not None:
            next_comment = next_parent_comment
        else:
            prev_comment = Comment.objects.filter(updated_at__gt=comment.updated_at).exclude(parent_comment__isnull=False).order_by('updated_at').first()
            next_comment = Comment.objects.filter(updated_at__lt=comment.updated_at).exclude(parent_comment__isnull=False).order_by('-updated_at').first()

            if prev_comment is not None:
                prev_id = prev_comment.id
            else:
                prev_id = False
            if next_comment is not None:
                next_id = next_comment.id
            else:
                next_id = False
            context['prev_id'] = prev_id
            context['next_id'] = next_id

    return render(request, 'comments/show.html', context)


# いいね機能
@login_required
@require_http(['GET', 'POST'])
def comments_like(request, comment_id):
    user = request.user

    if request.method == 'GET':
        comment = get_object_or_404(Comment, id=comment_id)
        existing_like = Like.objects.filter(target=comment, user=user).first()

        if existing_like:
            liked = True
        else:
            liked = False

        like_count = Like.objects.filter(target=comment).count()

        response_data = {
            'liked': liked,
            'like_count': like_count,
        }

        return JsonResponse(response_data)

    else:
        if comment_id:
            comment = get_object_or_404(Comment, id=comment_id)
            existing_like = Like.objects.filter(target=comment, user=user).first()

            if existing_like:
                existing_like.delete()
                liked = False
            else:
                like = Like(target=comment, user=user)
                like.save()
                liked = True

            like_count = Like.objects.filter(target=comment).count()
            
            response_data = {
                'liked': liked,
                'like_count': like_count,
            }
        
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)