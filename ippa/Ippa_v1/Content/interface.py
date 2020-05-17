from django.db import transaction
from datetime import datetime

from Content.exceptions import TournamentCreationFailed
from Content.models import Tournaments

def bulk_tournament_create(tournament_data):

	tournament_obj_list = list()
	try:
		with transaction.atomic():
			for tournament in tournament_data:
				network_name = tournament.get("Network")
				previous_tour_obj = Tournaments.objects.filter(network_name=network_name,
																is_deleted=0)
				if previous_tour_obj:
					previous_tour_obj.update(is_deleted=1)

				tournament_date = datetime.strptime(tournament.get("Date"), "%d-%m-%Y")
				tournament_detail = {
					"tournament_date":tournament_date,
					"event_name":tournament.get("Event Name"),
					"buy_in":tournament.get("Buy In"),
					"guaranteed":tournament.get("Guaranteed"),
					"network_name":tournament.get("Network"),
				}
				tournament_obj = Tournaments.objects.create_tournament(**tournament_detail)
				tournament_obj_list.append(tournament_obj)
			Tournaments.objects.bulk_create(tournament_obj_list)
		return True
	except Exception as ex:
		raise TournamentCreationFailed(str(ex))