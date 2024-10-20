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
  PlexPublicWithDirectories,
  PlexServerCreate,
} from '../models/index';
import {
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
    PlexPublicWithDirectoriesFromJSON,
    PlexPublicWithDirectoriesToJSON,
    PlexServerCreateFromJSON,
    PlexServerCreateToJSON,
} from '../models/index';

export interface CreatePlexServerApiPlexServerPostRequest {
    plexServerCreate: PlexServerCreate;
}

export interface DeletePlexServerApiPlexServerPlexIdDeleteRequest {
    plexId: number;
}

/**
 * 
 */
export class PlexApi extends runtime.BaseAPI {

    /**
     * Create Plex Server
     */
    async createPlexServerApiPlexServerPostRaw(requestParameters: CreatePlexServerApiPlexServerPostRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<PlexPublicWithDirectories>>> {
        if (requestParameters['plexServerCreate'] == null) {
            throw new runtime.RequiredError(
                'plexServerCreate',
                'Required parameter "plexServerCreate" was null or undefined when calling createPlexServerApiPlexServerPost().'
            );
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/api/plex_server`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: PlexServerCreateToJSON(requestParameters['plexServerCreate']),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(PlexPublicWithDirectoriesFromJSON));
    }

    /**
     * Create Plex Server
     */
    async createPlexServerApiPlexServerPost(requestParameters: CreatePlexServerApiPlexServerPostRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<PlexPublicWithDirectories>> {
        const response = await this.createPlexServerApiPlexServerPostRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Delete Plex Server
     */
    async deletePlexServerApiPlexServerPlexIdDeleteRaw(requestParameters: DeletePlexServerApiPlexServerPlexIdDeleteRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<any>> {
        if (requestParameters['plexId'] == null) {
            throw new runtime.RequiredError(
                'plexId',
                'Required parameter "plexId" was null or undefined when calling deletePlexServerApiPlexServerPlexIdDelete().'
            );
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/plex_server/{plex_id}`.replace(`{${"plex_id"}}`, encodeURIComponent(String(requestParameters['plexId']))),
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
     * Delete Plex Server
     */
    async deletePlexServerApiPlexServerPlexIdDelete(requestParameters: DeletePlexServerApiPlexServerPlexIdDeleteRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<any> {
        const response = await this.deletePlexServerApiPlexServerPlexIdDeleteRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Plex Server
     */
    async plexServerApiPlexServerGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<PlexPublicWithDirectories>>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/plex_server`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(PlexPublicWithDirectoriesFromJSON));
    }

    /**
     * Plex Server
     */
    async plexServerApiPlexServerGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<PlexPublicWithDirectories>> {
        const response = await this.plexServerApiPlexServerGetRaw(initOverrides);
        return await response.value();
    }

}
