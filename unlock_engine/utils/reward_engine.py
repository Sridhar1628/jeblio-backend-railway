import random

from unlock_engine.models.reward_models import Reward


def assign_reward(campaign):

    rewards = Reward.objects.filter(
        campaign=campaign,
        is_active=True,
        remaining_quantity__gt=0
    )

    if not rewards.exists():
        return None

    weighted_rewards = []

    for reward in rewards:

        weighted_rewards.extend(
            [reward] * reward.probability_weight
        )

    selected_reward = random.choice(weighted_rewards)

    selected_reward.remaining_quantity -= 1
    selected_reward.claimed_quantity += 1
    selected_reward.total_claims += 1

    selected_reward.save()

    return selected_reward