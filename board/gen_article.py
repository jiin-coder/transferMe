from .models import Article


def gen_master_article(apps, schema_editor):
    for article_id in range(1, 4):
        title = f"제목{id}"
        body = f"내용{id}"
        one_source = f"출처명{id}"
        information_source = f"출처링크{id}"


        Article.objects.create_article(
            title=title,
            body=body,
            one_source=one_source,
            information_source=information_source
        )