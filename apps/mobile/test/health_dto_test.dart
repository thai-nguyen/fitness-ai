import 'package:flutter_test/flutter_test.dart';
import 'package:fitness_ai_mobile/features/health/data/health_dto.dart';

void main() {
  test('parses readiness JSON', () {
    final dto = HealthReadyDto.fromJson({
      'status': 'ready',
      'service': 'fitness-ai-backend',
      'version': '0.1.0',
      'checks': {'database': 'up'},
    });
    final domain = dto.toDomain(checkedAt: DateTime.utc(2026, 11, 25));
    expect(domain.backendStatus, 'ready');
    expect(domain.service, 'fitness-ai-backend');
    expect(domain.version, '0.1.0');
    expect(domain.databaseStatus, 'up');
    expect(domain.isReady, isTrue);
  });
}
