from core.planner import Planner

context = {
    'merchant': {},
    'customer': {},
    'trigger': {
        'kind': 'perf_dip',
        'payload': {'topic': 'dentist', 'offer': '20% off', 'lead': 'urgent'}
    }
}
decision = {
    'audience': 'merchant',
    'intent': 'inform',
    'goal': 'increase appointments',
    'priority': 'high',
    'strategy': 'promote'
}
evidence = {
    'merchant_name': 'Asha',
    'owner_name': 'Asha',
    'customer_name': 'Priya',
    'category_slug': 'dentists',
    'has_active_offer': True,
    'merchant_engaged': True,
    'trigger_payload': {'topic': 'dentist', 'offer': '20% off'},
    'performance': {'views': 120, 'ctr': 0.8},
    'offers': [{'price': 499}]
}
plan = Planner().build_plan(context, decision, evidence)
print(plan['facts'])
