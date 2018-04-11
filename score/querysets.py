from django.db.models import QuerySet, Prefetch

class ScoreOwnerQueryset(QuerySet):

    def order_by_rank(self):
        queryset = self.filter(
                rank__gt = 0
            ).order_by(
                'rank'
            )
        return queryset

    def prefetch_scores(self):
        criterion_category_score_prefetcher = self.get_criterion_category_score_prefetcher()
        criterion_score_prefetcher = self.get_criterion_score_prefetcher()
        new_queryset = self.prefetch_related(
                criterion_category_score_prefetcher,
                criterion_score_prefetcher
            )
        return new_queryset

    def prefetch_criterion_category_scores(self):
        criterion_category_score_prefetcher = self.get_criterion_category_score_prefetcher()
        new_queryset = self.prefetch_related(
                criterion_category_score_prefetcher,
            )
        return new_queryset

    def get_criterion_category_score_prefetcher(self):
        related_score_model = self.get_related_criterion_category_score_model()
        prefetcher = Prefetch(
            "criterion_category_scores",
            queryset = related_score_model.objects.order_by(
                    "-criterion_category__university_only",
                    "criterion_category_id"
                ).select_related(
                    'criterion_category'
                )
        )
        return prefetcher

    def get_criterion_score_prefetcher(self):
        related_score_model = self.get_related_criterion_score_model()
        prefetcher = Prefetch(
            "criterion_scores", 
            queryset = related_score_model.objects.select_related(
                    'criterion'
                )
        )
        return prefetcher

    def get_related_criterion_category_score_model(self):
        model = self.model
        related_criterion_category_score_model = model._meta.get_field("criterion_category_scores").related_model
        return related_criterion_category_score_model

    def get_related_criterion_score_model(self):
        model = self.model
        related_criterion_score_model = model._meta.get_field("criterion_scores").related_model
        return related_criterion_score_model