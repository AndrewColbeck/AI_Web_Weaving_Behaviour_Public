from Models import Action

SPIDER_ACTIONS = [
    Action('sit', effects={'hunger': +1}),
    Action('seek', effects={'hunger': +2})
]
