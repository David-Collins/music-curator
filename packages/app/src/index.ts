import snoowrap from 'snoowrap';
import { TwitterApi } from 'twitter-api-v2';
import { SSMClient, GetParameterCommand } from '@aws-sdk/client-ssm';

export type AuthenticationData = {
  TWITTER_CONSUMER_KEY: string;
  TWITTER_CONSUMER_SECRET: string;
  TWITTER_OAUTH_TOKEN: string;
  TWITTER_OAUTH_TOKEN_SECRET: string;
  REDDIT_CLIENT_ID: string;
  REDDIT_CLIENT_SECRET: string;
  REDDIT_USERNAME: string;
  REDDIT_PASSWORD: string;
  REDDIT_USER_AGENT: string;
};

export async function getAuthData(): Promise<AuthenticationData> {
  const client = new SSMClient({ region: 'us-east-1' });
  const data = await client.send(
    new GetParameterCommand({
      Name: process.env.AUTH_PARAM,
      WithDecryption: true,
    })
  );
  const dataString = data.Parameter.Value ?? '';
  return JSON.parse(dataString);
}

export async function getRecentTweets(client: TwitterApi) {
  return (await client.v1.userTimelineByUsername('dc_music_tweets')).tweets.map(
    (x) => x.full_text.split('\n')[0]
  );
}

export async function handler(): Promise<void> {
  try {
    // Pull in all authentication data
    const authData = await getAuthData();
    // Authenticate into Reddit
    const redditClient = new snoowrap({
      userAgent: authData.REDDIT_USER_AGENT,
      clientId: authData.REDDIT_CLIENT_ID,
      clientSecret: authData.REDDIT_CLIENT_SECRET,
      username: authData.REDDIT_USERNAME,
      password: authData.REDDIT_PASSWORD,
    });
    // Authenticate into Twitter
    const twitterClient = new TwitterApi({
      appKey: authData.TWITTER_CONSUMER_KEY,
      appSecret: authData.TWITTER_CONSUMER_SECRET,
      accessToken: authData.TWITTER_OAUTH_TOKEN,
      accessSecret: authData.TWITTER_OAUTH_TOKEN_SECRET,
    });

    const recentTweets = await getRecentTweets(twitterClient);

    const subInfo = redditClient.getSubreddit('trap');
    const topPosts = (await subInfo.getTop({ time: 'week' })).filter(
      (x) =>
        (x.url.includes('soundcloud') || x.url.includes('spotify')) &&
        !recentTweets.includes(x.title)
    );

    if (topPosts.length) {
      const topEligblePost = topPosts[0];
      await twitterClient.v1.tweet(
        `${topEligblePost.title}\n${topEligblePost.url}`
      );
    }
  } catch (err) {
    console.log(err);
  }
}
