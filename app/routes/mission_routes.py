from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.shopping_mission_service import ShoppingMissionService
from app.repositories.mission_repository import MissionRepository

mission_bp = Blueprint('mission_views', __name__)
mission_api_bp = Blueprint('mission_api', __name__, url_prefix='/api/missions')
mission_service = ShoppingMissionService()
mission_repo = MissionRepository()


@mission_bp.route('/missions')
@login_required
def missions_list():
    missions = mission_repo.get_by_user(current_user.id)
    return render_template('missions/missions_list.html', missions=missions)


@mission_api_bp.route('/build', methods=['POST'])
@login_required
def api_build_mission():
    data = request.get_json() or {}
    prompt = data.get('prompt', '').strip()
    target_budget = float(data.get('target_budget', 30000.0))
    mode = data.get('optimization_mode', 'balanced')

    if not prompt or target_budget <= 0:
        return jsonify({'error': 'Valid prompt and budget are required'}), 400

    mission_data = mission_service.build_mission(current_user.id, prompt, target_budget, mode)
    return jsonify({'success': True, 'mission': mission_data})
