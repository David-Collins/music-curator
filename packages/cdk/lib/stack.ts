import { dirname } from 'path';
import { Duration, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';

export class MusicCuratorStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const paramAccess = new iam.PolicyStatement({
      actions: ['ssm:GetParameter'],
      resources: [
        this.formatArn({
          service: 'ssm',
          resource: 'parameter',
          account: '*',
          region: '*',
          resourceName: process.env.AUTH_PARAM_PATH,
        }),
      ],
    });

    const handler = new lambda.Function(this, 'Function', {
      code: lambda.Code.fromAsset(
        dirname(require.resolve('music-curator-app'))
      ),
      handler: 'index.handler',
      runtime: lambda.Runtime.NODEJS_14_X,
      environment: {
        AUTH_PARAM: `/${process.env.AUTH_PARAM_PATH}`,
      },
      initialPolicy: [paramAccess],
    });

    const schedule = new events.Rule(this, 'Schedule', {
      schedule: events.Schedule.rate(Duration.days(1)),
    });

    schedule.addTarget(new targets.LambdaFunction(handler));
  }
}
