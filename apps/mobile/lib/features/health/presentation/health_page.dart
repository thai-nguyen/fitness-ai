import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:fitness_ai_mobile/app/dependency_injection/injection.dart';
import 'package:fitness_ai_mobile/core/config/app_config.dart';
import 'package:fitness_ai_mobile/features/health/domain/health_status.dart';
import 'package:fitness_ai_mobile/features/health/presentation/cubit/health_cubit.dart';
import 'package:fitness_ai_mobile/features/health/presentation/cubit/health_state.dart';

class HealthPage extends StatelessWidget {
  const HealthPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => getIt<HealthCubit>()..check(),
      child: const _HealthView(),
    );
  }
}

class _HealthView extends StatelessWidget {
  const _HealthView();

  @override
  Widget build(BuildContext context) {
    final appName = getIt<AppConfig>().appName;
    return Scaffold(
      appBar: AppBar(title: Text(appName)),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: BlocBuilder<HealthCubit, HealthState>(
          builder: (context, state) {
            return switch (state) {
              HealthInitial() || HealthLoading() => const Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    CircularProgressIndicator(),
                    SizedBox(height: 16),
                    Text('Checking backend…'),
                  ],
                ),
              ),
              HealthSuccess(:final status) => _SuccessBody(status: status),
              HealthFailureState(:final message) => _ErrorBody(
                message: message,
              ),
            };
          },
        ),
      ),
    );
  }
}

class _SuccessBody extends StatelessWidget {
  const _SuccessBody({required this.status});

  final HealthStatus status;

  @override
  Widget build(BuildContext context) {
    final checked = status.checkedAt?.toLocal().toIso8601String() ?? 'n/a';
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Backend connection',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: 12),
        Text('Status: ${status.backendStatus}'),
        Text('Service: ${status.service}'),
        Text('Version: ${status.version}'),
        Text('Database: ${status.databaseStatus}'),
        Text('Last successful check: $checked'),
        const SizedBox(height: 24),
        FilledButton(
          onPressed: () => context.read<HealthCubit>().check(),
          child: const Text('Retry'),
        ),
      ],
    );
  }
}

class _ErrorBody extends StatelessWidget {
  const _ErrorBody({required this.message});

  final String message;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Backend connection',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: 12),
        Text(
          'Status: unavailable',
          style: TextStyle(color: Theme.of(context).colorScheme.error),
        ),
        Text(message),
        const SizedBox(height: 24),
        FilledButton(
          onPressed: () => context.read<HealthCubit>().check(),
          child: const Text('Retry'),
        ),
      ],
    );
  }
}
