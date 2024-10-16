/* eslint-disable */
/**
 * Engawa
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import * as runtime from '../runtime';
import type {
  HTTPValidationError,
  Subscription,
  SubscriptionCreate,
  SubscriptionCreateV2,
  Video,
} from '../models/index';
import {
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
    SubscriptionFromJSON,
    SubscriptionToJSON,
    SubscriptionCreateFromJSON,
    SubscriptionCreateToJSON,
    SubscriptionCreateV2FromJSON,
    SubscriptionCreateV2ToJSON,
    VideoFromJSON,
    VideoToJSON,
} from '../models/index';

export interface CreateSubscriptionApiSubscriptionPostRequest {
    subscriptionCreate: SubscriptionCreate;
}

export interface CreateSubscriptionV2ApiSubscriptionV2PostRequest {
    subscriptionCreateV2: SubscriptionCreateV2;
}

export interface DeleteSubscriptionApiSubscriptionSubscriptionIdDeleteRequest {
    subscriptionId: number;
}

export interface GetSubscriptionApiSubscriptionSubscriptionIdGetRequest {
    subscriptionId: number;
}

export interface GetSubscriptionVideosApiSubscriptionSubscriptionIdVideosGetRequest {
    subscriptionId: number;
}

export interface GetYoutubeChannelInfoApiYoutubeChannelInfoGetRequest {
    channelUrl: string;
}

export interface SyncSubscriptionApiSubscriptionSubscriptionIdSyncPostRequest {
    subscriptionId: number;
}

/**
 * 
 */
export class SubscriptionApi extends runtime.BaseAPI {

    /**
     * Create Subscription
     */
    async createSubscriptionApiSubscriptionPostRaw(requestParameters: CreateSubscriptionApiSubscriptionPostRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<any>> {
        if (requestParameters['subscriptionCreate'] == null) {
            throw new runtime.RequiredError(
                'subscriptionCreate',
                'Required parameter "subscriptionCreate" was null or undefined when calling createSubscriptionApiSubscriptionPost().'
            );
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/api/subscription`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: SubscriptionCreateToJSON(requestParameters['subscriptionCreate']),
        }, initOverrides);

        if (this.isJsonMime(response.headers.get('content-type'))) {
            return new runtime.JSONApiResponse<any>(response);
        } else {
            return new runtime.TextApiResponse(response) as any;
        }
    }

    /**
     * Create Subscription
     */
    async createSubscriptionApiSubscriptionPost(requestParameters: CreateSubscriptionApiSubscriptionPostRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<any> {
        const response = await this.createSubscriptionApiSubscriptionPostRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Create Subscription V2
     */
    async createSubscriptionV2ApiSubscriptionV2PostRaw(requestParameters: CreateSubscriptionV2ApiSubscriptionV2PostRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<any>> {
        if (requestParameters['subscriptionCreateV2'] == null) {
            throw new runtime.RequiredError(
                'subscriptionCreateV2',
                'Required parameter "subscriptionCreateV2" was null or undefined when calling createSubscriptionV2ApiSubscriptionV2Post().'
            );
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/api/subscription/v2`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: SubscriptionCreateV2ToJSON(requestParameters['subscriptionCreateV2']),
        }, initOverrides);

        if (this.isJsonMime(response.headers.get('content-type'))) {
            return new runtime.JSONApiResponse<any>(response);
        } else {
            return new runtime.TextApiResponse(response) as any;
        }
    }

    /**
     * Create Subscription V2
     */
    async createSubscriptionV2ApiSubscriptionV2Post(requestParameters: CreateSubscriptionV2ApiSubscriptionV2PostRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<any> {
        const response = await this.createSubscriptionV2ApiSubscriptionV2PostRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Delete All Subscriptions
     */
    async deleteAllSubscriptionsApiSubscriptionDeleteRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<any>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/subscription`,
            method: 'DELETE',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        if (this.isJsonMime(response.headers.get('content-type'))) {
            return new runtime.JSONApiResponse<any>(response);
        } else {
            return new runtime.TextApiResponse(response) as any;
        }
    }

    /**
     * Delete All Subscriptions
     */
    async deleteAllSubscriptionsApiSubscriptionDelete(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<any> {
        const response = await this.deleteAllSubscriptionsApiSubscriptionDeleteRaw(initOverrides);
        return await response.value();
    }

    /**
     * Delete Subscription
     */
    async deleteSubscriptionApiSubscriptionSubscriptionIdDeleteRaw(requestParameters: DeleteSubscriptionApiSubscriptionSubscriptionIdDeleteRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<any>> {
        if (requestParameters['subscriptionId'] == null) {
            throw new runtime.RequiredError(
                'subscriptionId',
                'Required parameter "subscriptionId" was null or undefined when calling deleteSubscriptionApiSubscriptionSubscriptionIdDelete().'
            );
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/subscription/{subscription_id}`.replace(`{${"subscription_id"}}`, encodeURIComponent(String(requestParameters['subscriptionId']))),
            method: 'DELETE',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        if (this.isJsonMime(response.headers.get('content-type'))) {
            return new runtime.JSONApiResponse<any>(response);
        } else {
            return new runtime.TextApiResponse(response) as any;
        }
    }

    /**
     * Delete Subscription
     */
    async deleteSubscriptionApiSubscriptionSubscriptionIdDelete(requestParameters: DeleteSubscriptionApiSubscriptionSubscriptionIdDeleteRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<any> {
        const response = await this.deleteSubscriptionApiSubscriptionSubscriptionIdDeleteRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get All Subscription
     */
    async getAllSubscriptionApiSubscriptionGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<Subscription>>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/subscription`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(SubscriptionFromJSON));
    }

    /**
     * Get All Subscription
     */
    async getAllSubscriptionApiSubscriptionGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<Subscription>> {
        const response = await this.getAllSubscriptionApiSubscriptionGetRaw(initOverrides);
        return await response.value();
    }

    /**
     * Get Subscription
     */
    async getSubscriptionApiSubscriptionSubscriptionIdGetRaw(requestParameters: GetSubscriptionApiSubscriptionSubscriptionIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Subscription>> {
        if (requestParameters['subscriptionId'] == null) {
            throw new runtime.RequiredError(
                'subscriptionId',
                'Required parameter "subscriptionId" was null or undefined when calling getSubscriptionApiSubscriptionSubscriptionIdGet().'
            );
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/subscription/{subscription_id}`.replace(`{${"subscription_id"}}`, encodeURIComponent(String(requestParameters['subscriptionId']))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => SubscriptionFromJSON(jsonValue));
    }

    /**
     * Get Subscription
     */
    async getSubscriptionApiSubscriptionSubscriptionIdGet(requestParameters: GetSubscriptionApiSubscriptionSubscriptionIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Subscription> {
        const response = await this.getSubscriptionApiSubscriptionSubscriptionIdGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get Subscription Videos
     */
    async getSubscriptionVideosApiSubscriptionSubscriptionIdVideosGetRaw(requestParameters: GetSubscriptionVideosApiSubscriptionSubscriptionIdVideosGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<Video>>> {
        if (requestParameters['subscriptionId'] == null) {
            throw new runtime.RequiredError(
                'subscriptionId',
                'Required parameter "subscriptionId" was null or undefined when calling getSubscriptionVideosApiSubscriptionSubscriptionIdVideosGet().'
            );
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/subscription/{subscription_id}/videos`.replace(`{${"subscription_id"}}`, encodeURIComponent(String(requestParameters['subscriptionId']))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(VideoFromJSON));
    }

    /**
     * Get Subscription Videos
     */
    async getSubscriptionVideosApiSubscriptionSubscriptionIdVideosGet(requestParameters: GetSubscriptionVideosApiSubscriptionSubscriptionIdVideosGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<Video>> {
        const response = await this.getSubscriptionVideosApiSubscriptionSubscriptionIdVideosGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get Youtube Channel Info
     */
    async getYoutubeChannelInfoApiYoutubeChannelInfoGetRaw(requestParameters: GetYoutubeChannelInfoApiYoutubeChannelInfoGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<any>> {
        if (requestParameters['channelUrl'] == null) {
            throw new runtime.RequiredError(
                'channelUrl',
                'Required parameter "channelUrl" was null or undefined when calling getYoutubeChannelInfoApiYoutubeChannelInfoGet().'
            );
        }

        const queryParameters: any = {};

        if (requestParameters['channelUrl'] != null) {
            queryParameters['channel_url'] = requestParameters['channelUrl'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/youtube_channel_info`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        if (this.isJsonMime(response.headers.get('content-type'))) {
            return new runtime.JSONApiResponse<any>(response);
        } else {
            return new runtime.TextApiResponse(response) as any;
        }
    }

    /**
     * Get Youtube Channel Info
     */
    async getYoutubeChannelInfoApiYoutubeChannelInfoGet(requestParameters: GetYoutubeChannelInfoApiYoutubeChannelInfoGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<any> {
        const response = await this.getYoutubeChannelInfoApiYoutubeChannelInfoGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Sync Subscription
     */
    async syncSubscriptionApiSubscriptionSubscriptionIdSyncPostRaw(requestParameters: SyncSubscriptionApiSubscriptionSubscriptionIdSyncPostRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Subscription>> {
        if (requestParameters['subscriptionId'] == null) {
            throw new runtime.RequiredError(
                'subscriptionId',
                'Required parameter "subscriptionId" was null or undefined when calling syncSubscriptionApiSubscriptionSubscriptionIdSyncPost().'
            );
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/subscription/{subscription_id}/sync`.replace(`{${"subscription_id"}}`, encodeURIComponent(String(requestParameters['subscriptionId']))),
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => SubscriptionFromJSON(jsonValue));
    }

    /**
     * Sync Subscription
     */
    async syncSubscriptionApiSubscriptionSubscriptionIdSyncPost(requestParameters: SyncSubscriptionApiSubscriptionSubscriptionIdSyncPostRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Subscription> {
        const response = await this.syncSubscriptionApiSubscriptionSubscriptionIdSyncPostRaw(requestParameters, initOverrides);
        return await response.value();
    }

}