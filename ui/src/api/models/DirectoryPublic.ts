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
import type { LocationPublic } from './LocationPublic';
import {
    LocationPublicFromJSON,
    LocationPublicFromJSONTyped,
    LocationPublicToJSON,
    LocationPublicToJSONTyped,
} from './LocationPublic';

/**
 * 
 * @export
 * @interface DirectoryPublic
 */
export interface DirectoryPublic {
    /**
     * 
     * @type {number}
     * @memberof DirectoryPublic
     */
    id?: number | null;
    /**
     * 
     * @type {string}
     * @memberof DirectoryPublic
     */
    title: string;
    /**
     * 
     * @type {string}
     * @memberof DirectoryPublic
     */
    uuid: string;
    /**
     * 
     * @type {number}
     * @memberof DirectoryPublic
     */
    key: number;
    /**
     * 
     * @type {Array<LocationPublic>}
     * @memberof DirectoryPublic
     */
    locations?: Array<LocationPublic>;
}

/**
 * Check if a given object implements the DirectoryPublic interface.
 */
export function instanceOfDirectoryPublic(value: object): value is DirectoryPublic {
    if (!('title' in value) || value['title'] === undefined) return false;
    if (!('uuid' in value) || value['uuid'] === undefined) return false;
    if (!('key' in value) || value['key'] === undefined) return false;
    return true;
}

export function DirectoryPublicFromJSON(json: any): DirectoryPublic {
    return DirectoryPublicFromJSONTyped(json, false);
}

export function DirectoryPublicFromJSONTyped(json: any, ignoreDiscriminator: boolean): DirectoryPublic {
    if (json == null) {
        return json;
    }
    return {
        
        'id': json['id'] == null ? undefined : json['id'],
        'title': json['title'],
        'uuid': json['uuid'],
        'key': json['key'],
        'locations': json['locations'] == null ? undefined : ((json['locations'] as Array<any>).map(LocationPublicFromJSON)),
    };
}

  export function DirectoryPublicToJSON(json: any): DirectoryPublic {
      return DirectoryPublicToJSONTyped(json, false);
  }

  export function DirectoryPublicToJSONTyped(value?: DirectoryPublic | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'id': value['id'],
        'title': value['title'],
        'uuid': value['uuid'],
        'key': value['key'],
        'locations': value['locations'] == null ? undefined : ((value['locations'] as Array<any>).map(LocationPublicToJSON)),
    };
}

