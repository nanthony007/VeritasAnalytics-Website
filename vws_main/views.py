from django.shortcuts import render
from django.db.models import Q, F, Avg, Sum, Count, Case, When, CharField, IntegerField, Value, FloatField, Func
from vws_main.models import Matchdata, Wrestler, Team, Event, FS_Event, FS_Wrestler, FS_Team, FS_Match
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView
from vws_main.filters import FS_RatingsFilter, FS_EventsFilter
from graphos.sources.model import ModelDataSource, SimpleDataSource
from graphos.renderers.gchart import LineChart
import pandas as pd


class Round(Func):
  function = 'ROUND'
  arity = 2


class FS_ReportsDetailView(DetailView):
    template_name = 'vws_main/reports_detail.html'
    slug_field = 'slug'

    def get_queryset(request):
        return FS_Wrestler.objects.filter().annotate(
            hi_rate=Avg('focus_wrestler2__hi_rate')*100,
            ho_rate=Avg('focus_wrestler2__ho_rate')*100,
            d_rate=Avg('focus_wrestler2__d_rate')*100,
            ls_rate=Avg('focus_wrestler2__ls_rate')*100,
            gb_rate=Avg('focus_wrestler2__gb_rate')*100,
            t_rate=Avg('focus_wrestler2__t_rate')*100,
            opp_hi_rate=Avg('focus_wrestler2__opp_hi_rate')*100,
            opp_ho_rate=Avg('focus_wrestler2__opp_ho_rate')*100,
            opp_d_rate=Avg('focus_wrestler2__opp_d_rate')*100,
            opp_ls_rate=Avg('focus_wrestler2__opp_ls_rate')*100,
            opp_gb_rate=Avg('focus_wrestler2__opp_gb_rate')*100,
            opp_t_rate=Avg('focus_wrestler2__opp_t_rate')*100,
            pin_count=Count('focus_wrestler2__result',
                filter=Q(focus_wrestler2__result='WinF')),
            tech_count=Count('focus_wrestler2__result',
                filter=Q(focus_wrestler2__result='WinTF')),
            win_count=Count('focus_wrestler2__result',
                filter=Q(focus_wrestler2__result='WinD')),
            loss_count=Count('focus_wrestler2__result',
                filter=Q(focus_wrestler2__result='LossD')),
            tech_loss_count=Count('focus_wrestler2__result',
                filter=Q(focus_wrestler2__result='LossTF')),
            fall_loss_count=Count('focus_wrestler2__result',
                filter=Q(focus_wrestler2__result='LossF')),
            match_count=Count('focus_wrestler2'),
        )


def home(request):
    return render(request, 'vws_main/home.html')


class FS_MatchDetailView(DetailView):
    queryset = FS_Match.objects.all().filter()
    template_name = "vws_main/fs_match_detail.html"


class FS_MatchTableView(ListView):
    queryset = FS_Match.objects.exclude(matchID__endswith='*').values('matchID', 'date', 'focus', 'opponent', 'focus_score', 'opp_score', 'result').order_by('-date', 'matchID')
    template_name = "vws_main/fs_matchdata_table.html"


class FS_WrestlerDetailView(DetailView):
    template_name = "vws_main/fs_wrestler_detail.html"
    slug_field = 'slug'
    queryset = FS_Wrestler.objects.filter().annotate(
        match_count=Count('focus_wrestler2'),
        avg_result=Avg(Case(
            When(focus_wrestler2__result='WinF', then=Value(1.75)),
            When(focus_wrestler2__result='WinTF', then=Value(1.50)),
            When(focus_wrestler2__result='WinMD', then=Value(1.25)),
            When(focus_wrestler2__result='WinD', then=Value(1.10)),
            When(focus_wrestler2__result='LossD', then=Value(0.90)),
            When(focus_wrestler2__result='LossMD', then=Value(0.75)),
            When(focus_wrestler2__result='LossTF', then=Value(0.50)),
            When(focus_wrestler2__result='LossF', then=Value(0.25)),
                output_field=FloatField())),
        # focus base stats
        hia=Sum('focus_wrestler2__hia'),
        hic2=Sum('focus_wrestler2__hic2'),
        hic4=Sum('focus_wrestler2__hic4'),
        hoa=Sum('focus_wrestler2__hoa'),
        hoc2=Sum('focus_wrestler2__hoc2'),
        hoc4=Sum('focus_wrestler2__hoc4'),
        da=Sum('focus_wrestler2__da'),
        dc2=Sum('focus_wrestler2__dc2'),
        dc4=Sum('focus_wrestler2__dc4'),
        lsa=Sum('focus_wrestler2__lsa'),
        lsc2=Sum('focus_wrestler2__lsc2'),
        lsc4=Sum('focus_wrestler2__lsc4'),
        gba=Sum('focus_wrestler2__gba'),
        gbc2=Sum('focus_wrestler2__gbc2'),
        ta=Sum('focus_wrestler2__ta'),
        tc2=Sum('focus_wrestler2__tc2'),
        tc4=Sum('focus_wrestler2__tc4'),
        exposure=Sum('focus_wrestler2__exposure'),
        gut=Sum('focus_wrestler2__gut'),
        leg_lace=Sum('focus_wrestler2__leg_lace'),
        turn=Sum('focus_wrestler2__turn'),

        # opp base stats
        opp_hia=Sum('focus_wrestler2__opp_hia'),
        opp_hic2=Sum('focus_wrestler2__opp_hic2'),
        opp_hic4=Sum('focus_wrestler2__opp_hic4'),
        opp_hoa=Sum('focus_wrestler2__opp_hoa'),
        opp_hoc2=Sum('focus_wrestler2__opp_hoc2'),
        opp_hoc4=Sum('focus_wrestler2__opp_hoc4'),
        opp_da=Sum('focus_wrestler2__opp_da'),
        opp_dc2=Sum('focus_wrestler2__opp_dc2'),
        opp_dc4=Sum('focus_wrestler2__opp_dc4'),
        opp_lsa=Sum('focus_wrestler2__opp_lsa'),
        opp_lsc2=Sum('focus_wrestler2__opp_lsc2'),
        opp_lsc4=Sum('focus_wrestler2__opp_lsc4'),
        opp_gba=Sum('focus_wrestler2__opp_gba'),
        opp_gbc2=Sum('focus_wrestler2__opp_gbc2'),
        opp_ta=Sum('focus_wrestler2__opp_ta'),
        opp_tc2=Sum('focus_wrestler2__opp_tc2'),
        opp_tc4=Sum('focus_wrestler2__opp_tc4'),
        opp_exposure=Sum('focus_wrestler2__opp_exposure'),
        opp_gut=Sum('focus_wrestler2__opp_gut'),
        opp_leg_lace=Sum('focus_wrestler2__opp_leg_lace'),
        opp_turn=Sum('focus_wrestler2__opp_turn'),

        # focus adv stats
        hi_rate=Avg('focus_wrestler2__hi_rate')*100,
        ho_rate=Avg('focus_wrestler2__ho_rate')*100,
        d_rate=Avg('focus_wrestler2__d_rate')*100,
        ls_rate=Avg('focus_wrestler2__ls_rate')*100,
        gb_rate=Avg('focus_wrestler2__gb_rate')*100,
        t_rate=Avg('focus_wrestler2__t_rate')*100,
        npf=Avg('focus_wrestler2__npf'),
        apm=Avg('focus_wrestler2__apm'),
        vs=Avg('focus_wrestler2__vs'),

        # opp adv stats
        opp_hi_rate=Avg('focus_wrestler2__opp_hi_rate')*100,
        opp_ho_rate=Avg('focus_wrestler2__opp_ho_rate')*100,
        opp_d_rate=Avg('focus_wrestler2__opp_d_rate')*100,
        opp_ls_rate=Avg('focus_wrestler2__opp_ls_rate')*100,
        opp_gb_rate=Avg('focus_wrestler2__opp_gb_rate')*100,
        opp_t_rate=Avg('focus_wrestler2__opp_t_rate')*100,
        opp_npf=Avg('focus_wrestler2__opp_npf'),
        opp_apm=Avg('focus_wrestler2__opp_apm'),
        opp_vs=Avg('focus_wrestler2__opp_vs'),

        # misc
        points_earned=Sum('focus_wrestler2__focus_score'),
        points_allowed=Sum('focus_wrestler2__opp_score'),
        # turn_rate=
        recovery=Sum('focus_wrestler2__recovery'),
        opp_recovery=Sum('focus_wrestler2__opp_recovery'),
        pushout=Sum('focus_wrestler2__pushout'),
        opp_pushout=Sum('focus_wrestler2__opp_pushout'),
        passive=Sum('focus_wrestler2__passive'),
        opp_passive=Sum('focus_wrestler2__opp_passive'),
        violation=Sum('focus_wrestler2__violation'),
        opp_violation=Sum('focus_wrestler2__opp_violation')
        )


class FS_TeamDetailView(DetailView):
    queryset = FS_Team.objects.all().order_by('-team_name.all.rating')
    template_name = 'vws_main/fs_team_detail.html'


class FS_EventsListView(ListView):
    queryset = FS_Event.objects.all()
    template_name = 'vws_main/fs_events_table.html'

    def get_queryset(self):
        return FS_Event.objects.values('name', 'date').distinct().order_by('-date')


class FS_EventsDetailView(DetailView):
    queryset = FS_Event.objects.all().order_by('-date')
    template_name = 'vws_main/fs_events_detail.html'


class FS_RatingsFilterView(FilterView):
    filterset_class = FS_RatingsFilter
    template_name = 'vws_main/fs_ratings.html'

    def get_queryset(request):
        return FS_Wrestler.objects.annotate(
            tier=Case(
                When(rating__gte=2500, then=Value('Grandmaster')),
                When(Q(rating__lt=2500) & Q(rating__gte=2300), then=Value('Master')),
                When(Q(rating__lt=2300) & Q(rating__gte=2000), then=Value('Expert')),
                When(Q(rating__lt=2000) & Q(rating__gte=1800), then=Value('Class A')),
                When(Q(rating__lt=1800) & Q(rating__gte=1600), then=Value('Class B')),
                When(Q(rating__lt=1600) & Q(rating__gte=1400), then=Value('Class C')),
                When(Q(rating__lt=1400) & Q(rating__gte=1200), then=Value('Class D')),
                When(Q(rating__lt=1200) & Q(rating__gte=1000), then=Value('Class E')),
                When(Q(rating__lt=1000) & Q(rating__gte=700), then=Value('Amateur')),
                When(rating__lt=700, then=Value('Novice')),
                output_field=CharField(),
            ),
            weight=Case(
                When(focus_wrestler2__weight=57, then=Value(57)),
                When(focus_wrestler2__weight=61, then=Value(61)),
                When(focus_wrestler2__weight=65, then=Value(65)),
                When(focus_wrestler2__weight=70, then=Value(70)),
                When(focus_wrestler2__weight=74, then=Value(74)),
                When(focus_wrestler2__weight=79, then=Value(79)),
                When(focus_wrestler2__weight=86, then=Value(86)),
                When(focus_wrestler2__weight=92, then=Value(92)),
                When(focus_wrestler2__weight=97, then=Value(97)),
                When(focus_wrestler2__weight=125, then=Value(125)),
                output_field=FloatField(),
            ),
            match_count=Count('focus_wrestler2__matchID')
            ).filter(match_count__gt=0).distinct().order_by('-rating')
