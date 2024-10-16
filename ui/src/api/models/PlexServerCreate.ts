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

import { mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface PlexServerCreate
 */
export interface PlexServerCreate {
    /**
     * 
     * @type {string}
     * @memberof PlexServerCreate
     */
    name: string;
    /**
     * 
     * @type {string}
     * @memberof PlexServerCreate
     */
    endpoint: string;
    /**
     * 
     * @type {string}
     * @memberof PlexServerCreate
     */
    port: string;
    /**
     * 
     * @type {string}
     * @memberof PlexServerCreate
     */
    token: string;
}

/**
 * Check if a given object implements the PlexServerCreate interface.
 */
export function instanceOfPlexServerCreate(value: object): value is PlexServerCreate {
    if (!('name' in value) || value['name'] === undefined) return false;
    if (!('endpoint' in value) || value['endpoint'] === undefined) return false;
    if (!('port' in value) || value['port'] === undefined) return false;
    if (!('token' in value) || value['token'] === undefined) return false;
    return true;
}

export function PlexServerCreateFromJSON(json: any): PlexServerCreate {
    return PlexServerCreateFromJSONTyped(json, false);
}

export function PlexServerCreateFromJSONTyped(json: any, ignoreDiscriminator: boolean): PlexServerCreate {
    if (json == null) {
        return json;
    }
    return {
        
        'name': json['name'],
        'endpoint': json['endpoint'],
        'port': json['port'],
        'token': json['token'],
    };
}

  export function PlexServerCreateToJSON(json: any): PlexServerCreate {
      return PlexServerCreateToJSONTyped(json, false);
  }

  export function PlexServerCreateToJSONTyped(value?: PlexServerCreate | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'name': value['name'],
        'endpoint': value['endpoint'],
        'port': value['port'],
        'token': value['token'],
    };
}

