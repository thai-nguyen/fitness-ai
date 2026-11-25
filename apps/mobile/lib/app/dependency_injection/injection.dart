import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:fitness_ai_mobile/core/config/app_config.dart';
import 'package:fitness_ai_mobile/core/network/dio_client.dart';
import 'package:fitness_ai_mobile/features/health/data/health_remote_data_source.dart';
import 'package:fitness_ai_mobile/features/health/data/health_repository_impl.dart';
import 'package:fitness_ai_mobile/features/health/domain/health_repository.dart';
import 'package:fitness_ai_mobile/features/health/presentation/cubit/health_cubit.dart';

final getIt = GetIt.instance;

void configureDependencies({AppConfig? config}) {
  if (getIt.isRegistered<AppConfig>()) {
    return;
  }

  final resolved = config ?? AppConfig.fromEnvironment();
  getIt.registerSingleton<AppConfig>(resolved);

  getIt.registerLazySingleton<Dio>(() => createDio(getIt<AppConfig>()));
  getIt.registerLazySingleton<HealthRemoteDataSource>(
    () => HealthRemoteDataSource(getIt<Dio>()),
  );
  getIt.registerLazySingleton<HealthRepository>(
    () => HealthRepositoryImpl(getIt<HealthRemoteDataSource>()),
  );
  getIt.registerFactory<HealthCubit>(
    () => HealthCubit(getIt<HealthRepository>()),
  );
}

void resetDependencies() {
  getIt.reset();
}
