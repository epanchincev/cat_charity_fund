from app.models import CharityProject, Donation


def calculate_invested_amount(
    donation: Donation,
    project: CharityProject,
) -> int:
    """Расчет размера доната"""
    if donation.balance_of_invested_amount >= project.amount_to_close:
        return project.amount_to_close

    return donation.balance_of_invested_amount
